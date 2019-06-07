import boto3
import xmltodict
import sys
import csv


def main(HITIDsfile):

    ''' Code to get results from a HIT published on Mechanical Turk. 
    Code is courtesy of AWS at 
    https://blog.mturk.com/tutorial-a-beginners-guide-to-crowdsourcing-ml-training-data-with-python-and-mturk-d8df4bdf2977
    Args HITIDsfile: this should be given when the code is run and is the path to a file containing the HITIDS, separated line by line, for all the HITs 
    you wish to retrieve results for.'''

    MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
    mturk = boto3.client('mturk',
       aws_access_key_id = "YOUR ACCESS KEY HERE",
       aws_secret_access_key = "YOUR SECRET ACCESS KEY HERE",
       region_name='us-east-1',
       # endpoint_url = MTURK_SANDBOX # to get results from the MTurk marketplace do not include endpoint_url at all
    )
	# You will need the following library
	# to help parse the XML answers supplied from MTurk
	# Install it in your local environment with
	# pip install xmltodict



    with open(HITIDsfile,'r') as input:

        ''' This loop is to get the results for every HIT that was published, so it checks the HITID for every HITID in the file.'''
        all_results = []    # this empty list will be filled with the Assignment result dictionaries provided by AWS. We will use this to write our output csv.
        for line in input:
            hit_id = line.strip()

            worker_results = mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Submitted']) # We only want HITs that have been 'Submitted' and thus have been completed by workers. 

            if worker_results['NumResults'] > 0:    # we only want to look at HITs that have a nonzero amount of results, otherwise the HIT remains to be done
               for assignment in worker_results['Assignments']:   # HITs can be published to be completed by multiple workers and we want to check the results for each worker who completes the HIT
                  xml_doc = xmltodict.parse(assignment['Answer'])
                  print("Worker's answer was:")
                  if type(xml_doc['QuestionFormAnswers']['Answer']) is list:
                     # Multiple fields in HIT layout
                     for answer_field in xml_doc['QuestionFormAnswers']['Answer']:      # loops through every input field that the worker gavea response for
                        print("For input field: " + answer_field['QuestionIdentifier'])
                        print("Submitted answer: " + answer_field['FreeText'])
                        assignment[answer_field['QuestionIdentifier']] = answer_field['FreeText']  # adds to the assignment dicionary the workers response to each input field
                  else:
                     # One field found in HIT layout
                     print("For input field: " + xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier'])
                     print("Submitted answer: " + xml_doc['QuestionFormAnswers']['Answer']['FreeText'])
                  all_results.append(assignment)
            else:
               print("No results ready yet")
        keys = ['AssignmentId','WorkerId','HITId','AssignmentStatus','AutoApprovalTime','AcceptTime','SubmitTime','Answer','response101','response102',
        'response103','response104','response105','response11','response12','response13','response14','response15',
        'response21','response22','response23','response24','response25',
        'response31','response32','response33','response34','response35',
        'response41','response42','response43','response44','response45',
        'response51','response52','response53','response54','response55',
        'response61','response62','response63','response64','response65',
        'response71','response72','response73','response74','response75',
        'response81','response82','response83','response84','response85',
        'response91','response92','response93','response94','response95']     # these are all of the necessary keys for our HIT

        with open("results_ouput.csv",'w') as output_file:                    # creates a csv with our results
          wr = csv.DictWriter(output_file,keys,restval="NA")
          wr.writeheader()
          wr.writerows(all_results)



if __name__=="__main__":
    main(sys.argv[1])
