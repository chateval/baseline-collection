#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:44:02 2019

@author: eddiecohen
"""

from jinja2 import Environment, FileSystemLoader, Template
import boto3
import sys


def main(inputfile):
  ''' Function to publish HITs for Collection Utterance on MTurk. Uses the HIT template found in templates/questions.xml.'''


  MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
  mturk = boto3.client('mturk',
     aws_access_key_id = "YOUR ACCESS KEY HERE",
     aws_secret_access_key = "YOUR SECRET ACCESS KEY HERE",
     region_name='us-east-1',
     endpoint_url = MTURK_SANDBOX  # to access MTurk marketplace leave out endpoint_url completely
  )
  # print("I have $" + mturk.get_account_balance()['AvailableBalance'] + " in my Sandbox account")

  # Actual HIT creation below 


  ''' Uses the templating engine jina. I made a template based off the Amazon MTurk given template for Collection Utterance and our design. 
  Template folder will be uploaded to github. 
  questions.xml is the xml form that publishes a HIT as provided by Amazon 
  at https://blog.mturk.com/tutorial-a-beginners-guide-to-crowdsourcing-ml-training-data-with-python-and-mturk-d8df4bdf2977
  I updated the basic template to use out HTML stlye, which is found in another template HIT.html
  Plan for future is to use jinja to refactor and take out the actual text of HIT.html '''

  fileloader = FileSystemLoader('templates')
  env = Environment(loader=fileloader)
  template = env.get_template("questions.xml") #

  HITlinks = [] # keeps track of HIT links for analysis purposes
  HITIDs = [] # keeps track of HIT ids for analysis purposes 

  allConversations = []
  responders = []

  with open(inputfile,'r') as input:
    for line in input:
      dialog = line.split("</s>")
      for i in range(len(dialog)):
        if i % 2 == 0:
          dialog[i] = "A: {}".format(dialog[i])
        else:
          dialog[i] = "B: {}".format(dialog[i])



      responder = ""

      if len(dialog) % 2 == 0:
        responder = "A"
      else:
        responder = "B"

      allConversations.append(dialog)
      responders.append(responder)


  for i in range(0,len(allConversations),10):



    output = template.render(convos=allConversations[i:i+10],responder=responders[i:i+10])

    with open('output.xml','w') as f:
      print(output,file=f)

    task = open(file='output.xml',mode='r').read()
    new_hit = mturk.create_hit(
        Title = 'Response Collection',
        Description = 'Provide at least two possible responses to ten given conversations. You may respond however you like but please provide at least two different responses.',
        Keywords = 'utterance, chat, language',
        Reward = '0.05',
        MaxAssignments = 5,
        LifetimeInSeconds = 604800,
        AssignmentDurationInSeconds = 10800,
        AutoApprovalDelayInSeconds = 172800,
        Question = task,
    )
    print("A new HIT has been created. You can preview it here:")
    print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
    print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")
    HITlinks.append(new_hit['HIT']['HITGroupId'])
    HITIDs.append(new_hit['HIT']['HITId'])


  with open(inputfile[0:len(inputfile)-4]+'HITIDs.txt','w') as f:
    for item in HITIDs:
      f.write("%s\n" % item)

  with open(inputfile[0:len(inputfile)-4]+'HITlinks.txt','w') as f:
    for item in HITlinks:
      f.write("%s\n" % item)

if __name__=="__main__":
  main(sys.argv[1])


# Remember to modify the URL above when you're publishing
# HITs to the live marketplace.
# Use: https://worker.mturk.com/mturk/preview?groupId=