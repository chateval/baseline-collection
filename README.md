Human Utterance Baseline Data Collection on Mechanical Turk
=======

Code to publish HITs on Mechanical Turk to collect human baselines for NLP tasks. A preview of the HITs can be found at: https://workersandbox.mturk.com/projects/3D3KZYB03KKA8YF604YHR2YT4EPV8B/tasks

## data
Contains the HIT results, jaccard analysis, and BLEU evaluation. 

## coverage_HITs
Contains all of the tracking information for the HITs that were published to guarantee we cover our dataset.

## analysis_code
Contains the code for fatigue analysis, Jaccard indexing, BLEU evaluation, and plotting the Jaccard and BLEU data to a histogram.

## BLEU_analysis
Contains the csvs with BLEU evaluation data for our HITs.

## fatigue_charts
Contains images of the scatter plots with best fit line for the fatigue of workers as they complete a HIT.

## analysis_charts
Contains the charts for Jaccard indexing and BLEU evaluation analysis.

## create_tasks.py
Contains the code for publishing HITs 
create_tasks takes four arguments.

arg1: txt file containing the conversations to post as HITs. Conversations can be any number of turns and do not need to all be the same number.  

arg2: path to desired output txt file for tracking HITIDs (used to get results). 

arg3: path to desired output txt file for tracking HIT links (to preview a batch). 

arg4: path to desired output csv file for tracking HITID -> conversations on HIT.
## get_results.py
Contains the code for checking the status of HITs published on Mechanical Turk, and retrieving the results for completed HITs. This code will be updated to store all of this information in a csv. Update: program stores all the results in an output csv.
get_results takes two arguments:

arg1: txt file containing the HITIDs to get results for.

arg2: path of desired output csv file.
## scrape_convos.py
Contains the code to scrape conversations to be used on MTurk from the following websites:
https://www.rong-chang.com/easyspeak/index.htm
https://www.eslfast.com/robot/
https://www.rong-chang.com/speak/
https://www.eslfast.com/easydialogs/index.html
## send_bonus.py
Contains the code for sending a bonus to a worker for completing more work than required. 
send_bonus requires 1 argument:

arg1: the csv file to read results from. a csv outputted from get_results is formatted correctly for this.
## templates
Contains two files.
## Results files
Contain the results from 2_turn and 3_turn HITs published on Mechanical Turk. These will be updated frequently.
## Tracking files
Map the HITID for a MTurk run to the conversations that were used for that HIT.

* **questions.xml** is the file containing the xml wrapper and the HTML for the HIT. 
* **HIT.html** is a general template that is being developed for HITs. The goal is to have this template be pretty bare and it will be filled on based on the required task using Python and Jinja2. 

---

The foundations for create_tasks.py, get_results.py, and questions.xml are courtesy of the tutorial from AWS found at: https://blog.mturk.com/tutorial-a-beginners-guide-to-crowdsourcing-ml-training-data-with-python-and-mturk-d8df4bdf2977


Any questions please contact: edcohen@seas.upenn.edu

