import boto3
import xmltodict
import sys


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
       endpoint_url = MTURK_SANDBOX # to get results from the MTurk marketplace do not include endpoint_url at all
    )
	# You will need the following library
	# to help parse the XML answers supplied from MTurk
	# Install it in your local environment with
	# pip install xmltodict



    with open(HITIDsfile,'r') as input:

        ''' This loop is to get the results for every HIT that was published, so it checks the HITID for every HITID in the file.'''

        for line in input:
            hit_id = line.strip()

            worker_results = mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Submitted']) # We only want HITs that have been 'Submitted' and thus have been completed by workers. 

            if worker_results['NumResults'] > 0:    # we only want to look at HITs that have a nonzero amount of results, otherwise the HIT remains to be done
               for assignment in worker_results['Assignments']:   # HITs can be published to be completed by multiple workers and we want to check the results for each worker who completes the HIT
                  xml_doc = xmltodict.parse(assignment['Answer'])
                  
                  print("Worker's answer was:")
                  if type(xml_doc['QuestionFormAnswers']['Answer']) is list:
                     # Multiple fields in HIT layout
                     for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
                        print("For input field: " + answer_field['QuestionIdentifier'])
                        print("Submitted answer: " + answer_field['FreeText'])
                  else:
                     # One field found in HIT layout
                     print("For input field: " + xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier'])
                     print("Submitted answer: " + xml_doc['QuestionFormAnswers']['Answer']['FreeText'])
            else:
               print("No results ready yet")


if __name__=="__main__":
    main(sys.argv[1])