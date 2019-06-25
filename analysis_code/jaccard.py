from jaccard_index.jaccard import jaccard_index
import csv
import sys
import statistics


def main(inputfile, num_assignments, outputfile):
    ''' Code to do analysis on the jaccard indices for HITs from MTurk
        Inputfile is the analysis file from get_results.py to be used for analysis
        Num_assignments is the number of times each HIT was assigned for this batch
        Outputfile is the desired .csv file to print the results to'''

    dict_keys = ["HITId"]
    dict_keys.extend(["prompt_{}_jaccard".format(i) for i in range(1,11)])
    dict_keys.append("HITJaccard")
    HIT_dict_list = []

    with open(inputfile, 'r') as input:
        reader = csv.reader(input)
        header = next(reader)
        rows = [row for row in reader]
        for i in range(0,len(rows),int(num_assignments)):
            HIT_dict = {}
            HIT_dict["HITId"] = rows[i][2]
            HIT_jaccards = []
            for j in range(9,59,5):
                prompt_jaccard = []
                for k in range(0,int(num_assignments)):
                    for y in range(k+1,int(num_assignments)):
                        prompt_jaccard.extend(jaccard_similarity(rows[i+k][j:j+5],rows[i+y][j:j+5]))
                jaccard_med = statistics.median(prompt_jaccard)
                HIT_dict["prompt_{}_jaccard".format(int(j / 5))] = jaccard_med
                HIT_jaccards.append(jaccard_med)
            HIT_dict["HITJaccard"] = statistics.median(HIT_jaccards)
            HIT_dict_list.append(HIT_dict)

    HIT_medians = []
    for HIT in HIT_dict_list:
        HIT_medians.append(HIT["HITJaccard"])


    HIT_dict_list.append({"HITId":"all_HITs","HITJaccard":statistics.median(HIT_medians)})


    with open(outputfile, 'w') as output:
        wr = csv.DictWriter(output, dict_keys)
        wr.writeheader()
        wr.writerows(HIT_dict_list)





            

def jaccard_similarity(list1, list2):
    ''' Computes the jaccard index for each pair of strings in list1 and list2
        Returns the list of jaccard indices'''
    jaccard_indices = []
    for s1 in list1:
        for s2 in list2:
            if s1!="NA" and s1!="." and s1!="" and s2!="NA" and s2!="." and s2!="":
                try:
                    jaccard_indices.append(jaccard_index(s1,s2))
                except:
                    print("No n-grams found. Appending zero for these two")
                    jaccard_indices.append(0)
    return jaccard_indices
   

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])