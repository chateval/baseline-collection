import csv
import sys
import os

'''
func txt_to_csv is for converting a txt file to a csv file where the first line of the txt file is the 
intended header for the csv with keys separated by commas. Every line in the txt file after is 
supposed to be a row in the csv with the values separated by commas.
Arg1: input txt file to format
Arg2: desired output csv file 
'''


def txt_to_csv(txt_file, csv_file):

    with open(txt_file,'r') as input:
        in_txt = csv.reader(input,delimiter='\t')
        header = next(in_txt)
        keys = header[0].split(",")
        all_rows = []
        for line in in_txt:
            linesplit = line[0].split(",\"")
            temp_dict = {}
            for i in range(len(linesplit)):
                temp_dict[keys[i]] = linesplit[i]
            all_rows.append(temp_dict)
                    
        with open(csv_file, 'w') as output:
            out_csv = csv.DictWriter(output,keys)
            out_csv.writeheader()
            out_csv.writerows(all_rows)	

        

if __name__=="__main__":
    txt_to_csv(sys.argv[1], sys.argv[2])