baseline-collection
=======

Code to publish HITs on Mechanical Turk to collect human baselines

## create_tasks.py
Contains the code for publishing HITs courtesy of the tutorial from aws at https://blog.mturk.com/tutorial-a-beginners-guide-to-crowdsourcing-ml-training-data-with-python-and-mturk-d8df4bdf2977

## templates
Contains two files.

* **questions.xml** is the file containing the xml wrapper for the HTML for the HIT. 
* **HIT.html** is a general template that is being developed for HITs. The goal is to have this template be pretty bare and it will be filled on based on the required task using Python and Jinja2. 

---

Any questions please contact: edcohen@seas.upenn.edu

