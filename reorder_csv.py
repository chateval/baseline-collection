import csv
import sys

def main(inputfile, outputfile):
    with open(inputfile, 'r') as input, open(outputfile, 'w') as output:
        keys = ['AssignmentId','WorkerId','HITId','AssignmentStatus','AutoApprovalTime','ApprovalTime','AcceptTime','SubmitTime','Answer','response11','response12','response13','response14','response15',
        'response21','response22','response23','response24','response25',
        'response31','response32','response33','response34','response35',
        'response41','response42','response43','response44','response45',
        'response51','response52','response53','response54','response55',
        'response61','response62','response63','response64','response65',
        'response71','response72','response73','response74','response75',
        'response81','response82','response83','response84','response85',
        'response91','response92','response93','response94','response95','response101','response102',
        'response103','response104','response105']
        writer = csv.DictWriter(output, fieldnames=keys)
        writer.writeheader()
        for row in csv.DictReader(input):
            writer.writerow(row)


if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])