#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:44:02 2019

@author: eddiecohen
"""

from jinja2 import Environment, FileSystemLoader, Template
import boto3
import sys
import csv


def main(inputfile):
  '''Function to publish HITs for Utterance Collection on MTurk
  Arg inputfile: this input file is the data that you want to use for your HIT. For example for an utterance collection task, this file should contains conversations
  separated by new lines, and turns within each conversation are separated by </s>'''

  MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
  mturk = boto3.client('mturk',
     aws_access_key_id = "YOUR ACCESS KEY HERE",
     aws_secret_access_key = "YOUR SECRET ACCESS KEY HERE",
     region_name='us-east-1',
     #endpoint_url = MTURK_SANDBOX  # to access MTurk marketplace leave out endpoint_url completely
  )
  # print("I have $" + mturk.get_account_balance()['AvailableBalance'] + " in my Sandbox account")

  # Actual HIT creation below 


  ''' Uses the templating engine jina. I made a template based off the Amazon MTurk given template for Collection Utterance and our design. 
  Template folder will be uploaded to github. 
  questions.xml is the xml form that publishes a HIT as provided by Amazon 
  at https://blog.mturk.com/tutorial-a-beginners-guide-to-crowdsourcing-ml-training-data-with-python-and-mturk-d8df4bdf2977
  I updated the basic template to use out HTML stlye, which is found in another template HIT.html
  Plan for future is to use jinja to refactor and take out the actual text of HIT.html '''

  fileloader = FileSystemLoader('templates')      # Accesses the directory 'templates' in the same classpath as this code file. 'templates' contains files for HTML/XML templates
  env = Environment(loader=fileloader)            # Establishes the environment to load a specific file from the templates diretory
  template = env.get_template("questions.xml")    # 'questions.xml' is the basic template which will be filled in. Here we access it, and we fill it when we call render

  HITlinks = [] # keeps track of HIT links for analysis purposes
  HITIDs = [] # keeps track of HIT ids for analysis purposes 

  allConversations = [] # list of lists of conversations. Each conversation is a list of the turns.
  responders = [] # list of who the worker is acing as as the responder for each conversation. 

  with open(inputfile,'r') as input:      
    for line in input:                      # this code formats the conversations into the style we want for the HIT
      dialog = line.split("</s>")
      for i in range(len(dialog)):
        if i % 2 == 0:                            
          dialog[i] = "A: {}".format(dialog[i])
        else:
          dialog[i] = "B: {}".format(dialog[i])    



      responder = ""

      if len(dialog) % 2 == 0:     # if there are #turn mod 2 = 0 turns in the convo, the worker is responding as person A
        responder = "A"
      else:
        responder = "B"            # otherwise the worker is responding as person B

      allConversations.append(dialog)
      responders.append(responder)

  tracking_dict_keys = ['HITID', 'convo_1', 'convo_2', 'convo_3', 'convo_4', 'convo_5', 'convo_6', 'convo_7', 'convo_8', 'convo_9', 'convo_10']  # these keys will be used to map HITID -> conversations

  tracking_dict_list = []                                                                                                                        # this list will contain the mapping for each HIT assignment

  for i in range(0,len(allConversations),10):       # HITs are created 10 conversations at a time. 



    output = template.render(convos=allConversations[i:i+10],responder=responders[i:i+10])    # fills the template with the conversations and responder info for the current HIT

    with open('output.xml','w') as f:
      print(output,file=f)

    task = open(file='output.xml',mode='r').read()
    new_hit = mturk.create_hit(
        Title = 'Response Collection',
        Description = 'Provide at least two possible responses to ten given conversations. A one cent bonus will be given for every response provided outside of the two required for each conversation.',
        Keywords = 'utterance, chat, language',
        Reward = '0.25',
        MaxAssignments = 3,
        LifetimeInSeconds = 604800,
        AssignmentDurationInSeconds = 1800,
        AutoApprovalDelayInSeconds = 172800,
        QualificationRequirements = [
          { 'QualificationTypeId':'00000000000000000040', 'Comparator':'GreaterThanOrEqualTo', 'IntegerValues':[100], 'RequiredToPreview':True}, 
          { 'QualificationTypeId':'000000000000000000L0', 'Comparator':'GreaterThan', 'IntegerValues':[97],'RequiredToPreview':True},
          { 'QualificationTypeId':'00000000000000000071', 'Comparator':'EqualTo', 'LocaleValues':[{'Country':'US'}], 'RequiredToPreview':True}],
        Question = task
    )

    print("A new HIT has been created. You can preview it here:")
    print("https://worker.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
    print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")

    HITlinks.append(new_hit['HIT']['HITGroupId'])
    HITIDs.append(new_hit['HIT']['HITId'])
    tracking_dict = {'HITID':new_hit['HIT']['HITId'], 'convo_1':allConversations[i], 'convo_2':allConversations[i+1], 'convo_3':allConversations[i+2], 'convo_4':allConversations[i+3], 'convo_5':allConversations[i+4],
    'convo_6':allConversations[i+5], 'convo_7':allConversations[i+6], 'convo_8':allConversations[i+7], 'convo_9':allConversations[i+8], 'convo_10':allConversations[i+9]}      # creates the tracking dictionary for the HIT assignment
    tracking_dict_list.append(tracking_dict)                        # adds the dictionary to our trackng dictonary list 




  # Code below records the HIT batch link and each individual HITID in text files for result gathering and analysis purposes a
  # Addition: code below also writes the csv that maps HITID -> conversations on the HIT

  with open(inputfile[0:len(inputfile)-4]+'MarketHITIDs_2.txt','w') as f:
    for item in HITIDs:
      f.write("%s\n" % item)

  with open(inputfile[0:len(inputfile)-4]+'MarketHITlinks_2.txt','w') as f:
    for item in HITlinks:
      f.write("%s\n" % item)

  with open(inputfile[0:len(inputfile)-4]+'HITTracking.csv','w') as f:              
    wr = csv.DictWriter(f,tracking_dict_keys)
    wr.writeheader()
    wr.writerows(tracking_dict_list)

if __name__=="__main__":        # Arg 1 should be the text file containing the conversations with turns separated by </s>
  main(sys.argv[1])


# Remember to modify the URL above when you're publishing
# HITs to the live marketplace.
# Use: https://worker.mturk.com/mturk/preview?groupId=
