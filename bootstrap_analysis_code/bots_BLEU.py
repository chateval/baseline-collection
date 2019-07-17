import os
import sys
import csv
import nltk
import itertools
import random
import statistics
from nltk.util import ngrams
from nltk.translate import bleu_score
from nltk.translate.bleu_score import SmoothingFunction


def main(promptsfile, inputdir, mturkfile, outputfile):
    '''Code for getting the BLEU scores for our bots against the NCM 1 turn data set
    Args:
    1. promptsfile containing the prompts from the data set separated by end line
    2. inputdir is the directory containing the txt files for each bots response to each of the prompts
    3. mturkfile is the mturk results file containing the human baseline responses to the prompts
    4. outputfile is the desired output csv for recording BLEU scores'''
    
    dict_keys = ["Model"]
    prompts = []
    with open(promptsfile, 'r') as promptsinput:
        for i,line in enumerate(promptsinput):
            dict_keys.append(line)
            dict_keys.append("Prompt {} BLEU".format(i+1))
            prompts.append(line)


    chencherry = SmoothingFunction()

    dict_dict = {}
    turkers = []
    start_index = -1
    end_index = -1
    ctr_index = -1
    with open(mturkfile, 'r') as mturk:
        reader = csv.reader(mturk)
        header = next(reader)
        start_index = header.index("response11")
        ctr_index = header.index("response21")
        end_index = header.index("response105")+1
        turkers.extend([row for row in reader])

    prompts_answers = []
    HIT_groups = itertools.groupby(turkers, key=lambda element: element[2])
    for i,group in enumerate(HIT_groups):
        assignments = list(group[1])
        for j in range(start_index,end_index,ctr_index-start_index):
            answers = []
            for assignment in assignments:
                answers.extend([response for response in assignment[j:j+5] if response!="NA" and response!="" and response!="."])
            prompts_answers.append(answers)

    for file in os.listdir(inputdir):
        if file!=".DS_Store" and file!="excludedbcunkown":
            bot = file[0:file.index(".txt")]
            filepath = os.path.join(inputdir,file)
            bot_responses = [] 
            with open(filepath, 'r') as bot_file:
                bot_responses = [line[0:line.find("\n")] if line.find("\n")!=-1 else line for line in bot_file]
            dict_dict[bot] = dict.fromkeys(dict_keys)
            bot_dict = dict_dict[bot]
            bot_dict["Model"] = bot
            
            for i,bot_response in enumerate(bot_responses):
                prompt_answers = prompts_answers[i]
                scores = []
                for j in range(10):
                    bootstrap_responses = random.sample(prompt_answers, 5)
                    bleu = bleu_score.sentence_bleu(bootstrap_responses,bot_response,smoothing_function=chencherry.method0)
                    scores.append(bleu)
                bot_dict[prompts[i]] = bot_response
                bot_dict["Prompt {} BLEU".format(i+1)] = statistics.mean(scores)

    dicts = dict_dict.values()
    with open(outputfile, 'w') as output:
        writer = csv.DictWriter(output, dict_keys)
        writer.writeheader()
        writer.writerows(dicts)







if __name__=="__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])