import sys
import nltk
import csv
import itertools
import statistics 
from nltk.util import ngrams
from nltk.translate import bleu_score
from nltk.translate.bleu_score import SmoothingFunction

def main(inputfile,outputfile):
    '''Gets BLEU sentence scores for responses
       Inputfile is the file produced by get_results.py
       Outpufile is the desired csv to print to
       Records BLEU scores as (min, max, median, standard deviation, number of responses)
       For HIT scores the HIT Id is recorded in both WorkerId and HITId for formattting purposes
       Currently using method1 for smoothing'''
    
    dict_keys = ["WorkerId", "HITId"]
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
        for i in range(10,60,5):
            HIT_BLEU = []
            responses = [(worker[1],response) for worker in workers for response in worker[i:i+5] if response!="NA"]
            for response in responses:
                worker = response[0]
                workerHIT_dict = dict_dict[(worker,group[0])]
                wo_response = [resp[1] for resp in responses if resp!=response]
                prompt = "prompt_{}".format(int((i-1)/5))
                bleu = bleu_score.sentence_bleu(wo_response,response[1],smoothing_function=chencherry.method1)
                if prompt in workerHIT_dict.keys():
                    workerHIT_dict[prompt].append(bleu)
                else:
                    workerHIT_dict[prompt] = [bleu]
                HIT_BLEU.append(bleu)
            HIT_dict["prompt_{}".format(int((i-1)/5))] = HIT_BLEU
        dict_dict[group[0]] = HIT_dict

    dict_list = dict_dict.values()
    for workerHIT_dict in dict_list:
        for i in range(1,11):
            prompt = 'prompt_{}'.format(i)
            try:
                workerHIT_dict[prompt] = (min(workerHIT_dict[prompt]),max(workerHIT_dict[prompt]),statistics.median(workerHIT_dict[prompt]), statistics.stdev(workerHIT_dict[prompt]), len(workerHIT_dict[prompt]))
            except:
                print("weird worker, moving on")


    with open(outputfile, 'w') as output:
        wr = csv.DictWriter(output,dict_keys)
        wr.writeheader()
        wr.writerows(dict_list)

if __name__=="__main__":
    main(sys.argv[1],sys.argv[2])