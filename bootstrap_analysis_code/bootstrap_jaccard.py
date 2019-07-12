from jaccard_index.jaccard import jaccard_index
import csv
import sys
import statistics
import random


def main(inputfile, outputfile, promptsfile):
    ''' Code to do analysis on the jaccard indices for HITs from MTurk
        Inputfile is the analysis file from get_results.py to be used for analysis
        num_conversations is the number of times each HIT was assigned for this batch
        Outputfile is the desired .csv file to print the results to'''

    dict_keys = ["WorkerId","HITId"]
    for i in range(1,11):
        dict_keys.extend(["prompt_{}".format(i), "prompt_{}_mean".format(i),"prompt_{}_median".format(i), "prompt_{}_min".format(i), "prompt_{}_max".format(i), 
            "prompt_{}_std".format(i), "prompt_{}_num_responses".format(i), "prompt_{}_responses".format(i), "prompt_{}_allJaccard".format(i), "prompt_{}_self_mean".format(i), "prompt_{}_self_median".format(i), "prompt_{}_self_min".format(i), "prompt_{}_self_max".format(i),
            "prompt_{}_self_std".format(i), "prompt_{}_self_num_responses".format(i), "prompt_{}_selfJaccard".format(i)])


    dict_keys.extend(["prompt_{}".format(i) for i in range(1,11)])
    HIT_dict_list = []

    rows = []
    with open(inputfile, 'r') as input:
        reader = csv.reader(input)
        header = next(reader)
        rows = [row for row in reader]

    prompt_start = header.index("response101")
    prompt_end = header.index("response95")+1
    print(prompt_start,prompt_end)
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

        for i in range(prompt_start,prompt_end,5): # goes through all five responses for each prompt and then moves on 

            HIT_Jaccard = []
            HIT_selfJaccard = []
            responses = [(worker[1],response) for worker in workers for response in worker[i:i+5] if response!="NA" and response!="." and response!=""]    # instantiates a list of tuple of the form (WorkerId,responses) recording the responses provided by each worker for this HIT
            prompt = "prompt_{}_allJaccard".format(int((i)/5)) # key where we store Jaccard scores against all responses
            self_prompt = "prompt_{}_selfJaccard".format(int((i)/5))   # key where we store Jaccard scores for a worker against himself
            num_responses = len(responses)

            for response in responses:  # loop through each response in our instantiated list to get the Jaccard score for that response
                
                worker = response[0]    # get the WorkerId of the worker who provided this response 
                proposed_response = response[1] # get the response that we are looking at specifically
                workerHIT_dict = dict_dict[(worker,HITId)]   # retrieve the worker's dictionary
                wo_response = [resp[1] for resp in responses if resp!=response] # instantiates a list of all of the responses to this HIT except for the response we are calculating the Jaccard score for
                worker_responses = [resp[1] for resp in responses if resp!=response and resp[0]==worker] # instantiates a list of all of the other responses to this HIT for this prompt provided by the worker who gave the response we are looking at
                response_Jaccard = []
                self_Jaccard = []

                for j in range(10):

                    bootstrap_responses = random.sample(wo_response, 7) # randomly gets either 5 or 7 of the responses to the prompt, not including current response. must be set manually based on which set is being used
                    response_Jaccard.append(jaccard_similarity(proposed_response,bootstrap_responses))

                    self_bootstrap_response = random.sample(worker_responses, 1)    # randomly gets one of this workers' other responses to the prompt to get the Jaccard aganst 
                    self_Jaccard = jaccard_index(response, self_bootstrap_response[0]) 
                    self_Jaccard.append(self_Jaccard)    

                response_mean = statistics.mean(response_Jaccard)
                self_mean = statistics.mean(self_Jaccard)
                if prompt in workerHIT_dict.keys(): # checks if this is not the first time we are writing a Jaccard score for this HIT and prompt for this worker
                    workerHIT_dict[prompt].append(response_mean)
                    workerHIT_dict[self_prompt].append(self_mean)
                else:
                    workerHIT_dict[prompt] = [response_mean]
                    workerHIT_dict[self_prompt] = [self_mean]
                
                HIT_Jaccard.append(response_mean)   # records the Jaccard score which will be used for the average Jaccard for this HIT for this prompt
                HIT_selfJaccard.append(self_Jaccard)

            HIT_dict[prompt] = HIT_Jaccard # sets the entry in the dicionary for  this HIT for this prompt to be the list of Jaccard scores
            HIT_dict[self_prompt] = HIT_selfJaccard
            #HIT_dict["prompt_{}_responses".format(int((i)/5))] = HIT_responses
        dict_dict[HITId] = HIT_dict     # updates that the HIT_dict is the dictionary we wish to use in our dictionary of dicionaries


    prompt_rows = []    # instantiates a list for recording the prompts from the promptsfile csv
    with open(promptsfile, 'r') as prompts:
        reader = csv.reader(prompts)
        prompt_rows.extend([row for row in reader])

    dict_list = dict_dict.values()  # retrieves all of the dictionaries in our dicitonary of dictionaries
    for workerHIT_dict in dict_list:    # for each dictionary in our dictionary we are going to set the statistics accordingly 
        for i in range(1,11):
            
            prompt = "prompt_{}_allJaccard".format(i)  # we do this for each prompt 1-10
            self_prompt = "prompt_{}_selfJaccard".format(i)
            
            try:    # tries to set the Worker or HIT dictionary (demarked by their Ids) to contain the median Jaccard for a HIT and prompt, the min, the max, the std, and the number of responses. As well as records what the actual prompt was from prompt_rows which was created earlier 
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

def jaccard_similarity(proposed_response, gt_responses):
    ''' Computes the mean jaccard index for the jaccard indices of proposed response against each of the gt-responses
        Returns the mean jaccard index'''

    jaccard_indices = []
    for response in gt_responses:
        try:
            jaccard_indices.append(jaccard_index(proposed_response,response))
        except:
            print("No n-grams found. Appending zero for these two")
            jaccard_indices.append(0)
    return statistics.mean(jaccard_indices)

# def jaccard_single_worker(list1):

#     jaccard_indices = []
#     for i in range(0,len(list1)):
#         for j in range(i+1,len(list1)):
#             s1 = list1[i]
#             s2 = list1[j]
#             if s1!="NA" and s1!="." and s1!="" and s2!="NA" and s2!="." and s2!="":
#                 try:
#                     jaccard_indices.append(jaccard_index(s1,s2))
#                 except:
#                     print("No n-grams found. Appending zero for these two")
#                     jaccard_indices.append(0)
#     return jaccard_indices   
   

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])