import sys
import nltk
import csv
import itertools
import statistics 
from nltk.util import ngrams
from nltk.translate import bleu_score
from nltk.translate.bleu_score import SmoothingFunction

def main(inputfile,outputfile, promptsfile):
    '''Gets BLEU sentence scores for responses
       Inputfile is the file produced by get_results.py
       Outpufile is the desired csv to print to
       Records BLEU scores as (min, max, median, standard deviation, number of responses)
       For HIT scores the HIT Id is recorded in both WorkerId and HITId for formattting purposes
       Currently using no smoothing'''
    
    dict_keys = ["WorkerId", "HITId"]
    for i in range(1,11):
        dict_keys.extend(["prompt_{}".format(i), "prompt_{}_BLEU".format(i), "prompt_{}_min".format(i), "prompt_{}_max".format(i), "prompt_{}_std".format(i), "prompt_{}_num_responses".format(i), "prompt_{}_allBLEU".format(i)])

    dict_keys.extend(["prompt_{}".format(i) for i in range(1,11)])
    chencherry = SmoothingFunction()

    rows = []
    with open(inputfile, 'r') as input:
        reader = csv.reader(input)
        header = next(reader)
        rows.extend([row for row in reader])

    HIT_groups = itertools.groupby(rows, key=lambda element: element[2])
    dict_dict = {}

    worker_groups = itertools.groupby(rows, key=lambda element: element[1])
    for worker in worker_groups:
        for HITs in worker[1]:
            dict_dict[(worker[0],HITs[2])] = {"WorkerId":worker[0],"HITId":HITs[2]}

    for group in HIT_groups:
        
        HIT_dict = {"WorkerId":group[0],"HITId":group[0]}
        workers = [worker for worker in group[1]]
        for i in range(9,59,5):
            HIT_BLEU = []
            responses = [(worker[1],response) for worker in workers for response in worker[i:i+5] if response!="NA"]
            for response in responses:
                worker = response[0]
                workerHIT_dict = dict_dict[(worker,group[0])]
                wo_response = [resp[1] for resp in responses if resp!=response]
                prompt = "prompt_{}_allBLEU".format(int((i)/5))
                bleu = bleu_score.sentence_bleu(wo_response,response[1],smoothing_function=chencherry.method0)
                if prompt in workerHIT_dict.keys():
                    workerHIT_dict[prompt].append(bleu)
                else:
                    workerHIT_dict[prompt] = [bleu]
                HIT_BLEU.append(bleu)
            HIT_dict["prompt_{}_allBLEU".format(int((i)/5))] = HIT_BLEU
        dict_dict[group[0]] = HIT_dict


    prompt_rows = []
    with open(promptsfile, 'r') as prompts:
        reader = csv.reader(prompts)
        prompt_rows.extend([row for row in reader])

    dict_list = dict_dict.values()
    for workerHIT_dict in dict_list:
        for i in range(1,11):
            prompt = "prompt_{}_allBLEU".format(i)
            try:
                workerHIT_dict["prompt_{}_BLEU".format(i)] = statistics.median(workerHIT_dict[prompt])
                workerHIT_dict["prompt_{}_min".format(i)] = min(workerHIT_dict[prompt])
                workerHIT_dict["prompt_{}_max".format(i)] = max(workerHIT_dict[prompt])
                workerHIT_dict["prompt_{}_std".format(i)] = statistics.stdev(workerHIT_dict[prompt])
                workerHIT_dict["prompt_{}_num_responses".format(i)] = len(workerHIT_dict[prompt])
                workerHIT_dict["prompt_{}".format(i)] = [HIT for HIT in prompt_rows if HIT[0]==workerHIT_dict["HITId"]][0][i]
            except:
                print("weird worker, moving on")


    with open(outputfile, 'w') as output:
        wr = csv.DictWriter(output,dict_keys)
        wr.writeheader()
        wr.writerows(dict_list)

if __name__=="__main__":
    main(sys.argv[1],sys.argv[2], sys.argv[3])
