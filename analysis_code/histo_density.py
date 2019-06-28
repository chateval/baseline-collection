import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import sys
import csv

def main(inputfile, num_assignments, data):

    rows = []
    start_index = -1
    end_index = -1
    with open(inputfile, 'r') as input:
        reader = csv.reader(input)
        header = next(reader)
        start_index = header.index("prompt_1_jaccard")
        end_index = header.index("prompt_10_jaccard") + 1
        rows = [row for row in reader]

    if data=="BLEU":

        BLEU_scores = []
        total_num = 0
        for row in rows[0:int(num_assignments)]:
            for i in range(start_index,end_index):
                split = row[i].split(", ")          # this split handles a formatting issue with the csv
                if len(split) > 4:
                    BLEU_scores.append(float(split[2])) # scores to be plotted in a histogram/density plot
                    total_num += int(split[4][0:len(split[4])-1])


        for i, binwidth in enumerate([1, 5, 10, 15]):
        
            # Set up the plot
            ax = plt.subplot(2, 2, i + 1)
            
            # Draw the plot
            ax.hist(BLEU_scores, bins = int(150/binwidth),
                     color = 'blue', edgecolor = 'black')

            #pd.Series(BLEU_scores).plot(kind='density')
            
            # Title and labels
            ax.set_title('Histogram with Binwidth = %d' % binwidth, size = 30)
            ax.set_xlabel('BLEU score', size = 22)
            ax.set_ylabel('Responses', size= 22)

        plt.tight_layout()
        plt.show()

        plt.show()

    else:
        Jaccard_indices = []
        total_num = 0
        for row in rows[0:int(num_assignments)]:
            for i in range(start_index,end_index):
                split = row[i].split(", ")          # this split handles a formatting issue with the csv
                Jaccard_indices.append(float(split[0][1:])) # scores to be plotted in a histogram/density plot
                total_num += int(split[2][0:len(split[2])-1])


        for i, binwidth in enumerate([1, 5, 10, 15]):
        
            # Set up the plot
            ax = plt.subplot(2, 2, i + 1)
            
            # Draw the plot
            ax.hist(Jaccard_indices, bins = int(150/binwidth),
                     color = 'blue', edgecolor = 'black')

            #pd.Series(BLEU_scores).plot(kind='density')
            
            # Title and labels
            ax.set_title('Histogram with Binwidth = %d' % binwidth, size = 30)
            ax.set_xlabel('Jaccard Index', size = 22)
            ax.set_ylabel('Responses', size= 22)

        plt.tight_layout()
        plt.show()

        plt.show() 

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])