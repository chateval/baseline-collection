import sys
import nltk
import csv
import itertools
import statistics
import random
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
        dict_keys.extend(["prompt_{}".format(i), "prompt_{}_mean".format(i),"prompt_{}_median".format(i), "prompt_{}_min".format(i), "prompt_{}_max".format(i), 
            "prompt_{}_std".format(i), "prompt_{}_num_responses".format(i), "prompt_{}_responses".format(i), "prompt_{}_allBLEU".format(i), "prompt_{}_self_mean".format(i), "prompt_{}_self_median".format(i), "prompt_{}_self_min".format(i), "prompt_{}_self_max".format(i),
            "prompt_{}_self_std".format(i), "prompt_{}_self_num_responses".format(i), "prompt_{}_selfBLEU".format(i)])

    dict_keys.extend(["prompt_{}".format(i) for i in range(1,11)])
    chencherry = SmoothingFunction()

    rows = []
    with open(inputfile, 'r') as input:
        reader = csv.reader(input)
        header = next(reader)
        rows.extend([row for row in reader])

    prompt_start = header.index("response101")
    prompt_end = header.index("response95")+1
    HIT_groups = itertools.groupby(rows, key=lambda element: element[2])    # groups results by HITId, so all assignments for a single HIT are now grouped 
    dict_dict = {}

    worker_groups = itertools.groupby(rows, key=lambda element: element[1]) # groups results by WorkerId, so all HITs a worker completed are now grouped
    
    for worker in worker_groups:
        for HITs in worker[1]:
            dict_dict[(worker[0],HITs[2])] = {"WorkerId":worker[0],"HITId":HITs[2]} # instantiates dictionaries for each worker containing their WorkerId and HITId they completed

    for group in HIT_groups:    # iterate through each HIT in our HIT groups
        
        HITId = group[0]    # get the HITId now for making code more readable later on 

        HIT_dict = {"WorkerId":group[0],"HITId":HITId}   # instantiates a dictionary for each HIT that contains the HITId recorded twice, as the WorkerId and as the HITId. This is done for formatting the output csv
        workers = [worker for worker in group[1]]   # instantiates the list of workers who completed assignments for this HIT
        
        for i in range(prompt_start,prompt_end,5): # 9 to 59 by 5 based on the csv outputted by get_results.py ****THIS SHOULD BE UPDATED TO BE FLEXIBLE BASED ON THE FIRST INDEX OF 'prompt_1' and last index of 'prompt_10'*****
            
            HIT_BLEU = []
            HIT_selfBLEU = []
            responses = [(worker[1],response) for worker in workers for response in worker[i:i+5] if response!="NA" and response!="." and response!=""]    # instantiates a list of tuple of the form (WorkerId,responses) recording the responses provided by each worker for this HIT
            prompt = "prompt_{}_allBLEU".format(int((i)/5)) # key where we store BLEU scores against all responses
            self_prompt = "prompt_{}_selfBLEU".format(int((i)/5))   # key where we store BLEU scores for a worker against himself
            num_responses = len(responses)

            for response in responses:  # loop through each response in our instantiated list to get the BLEU score for that response
                
                worker = response[0]    # get the WorkerId of the worker who provided this response 
                proposed_response = response[1] # get the response that we are looking at specifically
                workerHIT_dict = dict_dict[(worker,HITId)]   # retrieve the worker's dictionary
                wo_response = [resp[1] for resp in responses if resp!=response] # instantiates a list of all of the responses to this HIT except for the response we are calculating the BLEU score for
                worker_responses = [resp[1] for resp in responses if resp!=response and resp[0]==worker] # instantiates a list of all of the other responses to this HIT for this prompt provided by the worker who gave the response we are looking at
                response_BLEU = []
                self_BLEU = []
                
                # bootstrapping method to compare the response to a random sample with replacement of seven of the other responses, not including this response, to the prompt. also do bootstrap for self BLEU score 
                for j in range(10):
                    
                    bootstrap_responses = random.sample(wo_response, 7) # randomly gets either 5 or 7 of the responses to the prompt, not including current response. must be set manually based on which set is being used
                    bleu = bleu_score.sentence_bleu(bootstrap_responses,proposed_response,smoothing_function=chencherry.method0)  # gets the BLEU score for this response compared to all of the other responses for this HIT, using chencherry method 0
                    response_BLEU.append(bleu)

                    self_bootstrap_response = random.sample(worker_responses, 1)    # randomly gets one of this workers' other responses to the prompt to get the BLEU aganst 
                    self_bleu = bleu_score.sentence_bleu(self_bootstrap_response,proposed_response,smoothing_function=chencherry.method0)  
                    self_BLEU.append(self_bleu)                

                response_mean = statistics.mean(response_BLEU)
                self_mean = statistics.mean(self_BLEU)
                if prompt in workerHIT_dict.keys(): # checks if this is not the first time we are writing a BLEU score for this HIT and prompt for this worker
                    workerHIT_dict[prompt].append(response_mean)
                    workerHIT_dict[self_prompt].append(self_mean)
                else:
                    workerHIT_dict[prompt] = [response_mean]
                    workerHIT_dict[self_prompt] = [self_mean]
                
                HIT_BLEU.append(response_mean)   # records the bleu score which will be used for the average BLEU for this HIT for this prompt
                HIT_selfBLEU.append(self_bleu)

            HIT_dict[prompt] = HIT_BLEU # sets the entry in the dicionary for  this HIT for this prompt to be the list of BLEU scores
            HIT_dict[self_prompt] = HIT_selfBLEU
            #HIT_dict["prompt_{}_responses".format(int((i)/5))] = HIT_responses
        dict_dict[HITId] = HIT_dict     # updates that the HIT_dict is the dictionary we wish to use in our dictionary of dicionaries


    prompt_rows = []    # instantiates a list for recording the prompts from the promptsfile csv
    with open(promptsfile, 'r') as prompts:
        reader = csv.reader(prompts)
        prompt_rows.extend([row for row in reader])

    dict_list = dict_dict.values()  # retrieves all of the dictionaries in our dicitonary of dictionaries
    for workerHIT_dict in dict_list:    # for each dictionary in our dictionary we are going to set the statistics accordingly 
        for i in range(1,11):
            
            prompt = "prompt_{}_allBLEU".format(i)  # we do this for each prompt 1-10
            self_prompt = "prompt_{}_selfBLEU".format(i)
            
            try:    # tries to set the Worker or HIT dictionary (demarked by their Ids) to contain the median BLEU for a HIT and prompt, the min, the max, the std, and the number of responses. As well as records what the actual prompt was from prompt_rows which was created earlier 
                workerHIT_dict["prompt_{}_mean".format(i)] = statistics.mean(workerHIT_dict[prompt])
                workerHIT_dict["prompt_{}_median".format(i)] = statistics.median(workerHIT_dict[prompt])
                workerHIT_dict["prompt_{}_min".format(i)] = min(workerHIT_dict[prompt])
                workerHIT_dict["prompt_{}_max".format(i)] = max(workerHIT_dict[prompt])
                workerHIT_dict["prompt_{}_std".format(i)] = statistics.stdev(workerHIT_dict[prompt])
                workerHIT_dict["prompt_{}_num_responses".format(i)] = len(workerHIT_dict[prompt])
                workerHIT_dict["prompt_{}".format(i)] = [HIT for HIT in prompt_rows if HIT[0]==workerHIT_dict["HITId"]][0][i]
                workerHIT_dict["prompt_{}_self_mean".format(i)] = statistics.mean(workerHIT_dict[self_prompt])
                workerHIT_dict["prompt_{}_self_median".format(i)] = statistics.median(workerHIT_dict[self_prompt])
                workerHIT_dict["prompt_{}_self_min".format(i)] = min(workerHIT_dict[self_prompt])
                workerHIT_dict["prompt_{}_self_max".format(i)] = max(workerHIT_dict[self_prompt])
                workerHIT_dict["prompt_{}_self_std".format(i)] = statistics.stdev(workerHIT_dict[self_prompt])
                workerHIT_dict["prompt_{}_self_num_responses".format(i)] = len(workerHIT_dict[self_prompt])
            except:
                print("weird worker, moving on")


    with open(outputfile, 'w') as output:   # writes our dictionary to the desired csv outputfile using the keysv instantiated at the top of the file
        wr = csv.DictWriter(output,dict_keys)
        wr.writeheader()
        wr.writerows(dict_list)

if __name__=="__main__":
    main(sys.argv[1],sys.argv[2], sys.argv[3])