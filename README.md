baseline-collection
=======

Code to publish HITs on Mechanical Turk to collect human baselines for NLP tasks. A preview of the HITs can be found at: https://workersandbox.mturk.com/projects/3PJ6380TR3SRI5TCMJADV7G7ARFQFN/tasks?ref=w_pl_prvw

## create_tasks.py
Contains the code for publishing HITs 
## templates
Contains two files.

* **questions.xml** is the file containing the xml wrapper and the HTML for the HIT. 
* **HIT.html** is a general template that is being developed for HITs. The goal is to have this template be pretty bare and it will be filled on based on the required task using Python and Jinja2. 

---

Both create_tasks.py and questions.xml are courtesy of the tutorial from AWS found at: courtesy of the tutorial from aws at: https://blog.mturk.com/tutorial-a-beginners-guide-to-crowdsourcing-ml-training-data-with-python-and-mturk-d8df4bdf2977


Any questions please contact: edcohen@seas.upenn.edu

