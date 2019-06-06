baseline-collection
=======

Code to publish HITs on Mechanical Turk to collect human baselines for NLP tasks. A preview of the HITs can be found at: https://workersandbox.mturk.com/projects/3D3KZYB03KKA8YF604YHR2YT4EPV8B/tasks

## create_tasks.py
Contains the code for publishing HITs 
## get_results.py
Contains the code for checking the status of HITs published on Mechanical Turk, and retrieving the results for completed HITs. This code will be updated to store all of this information in a csv.
## templates
Contains two files.

* **questions.xml** is the file containing the xml wrapper and the HTML for the HIT. 
* **HIT.html** is a general template that is being developed for HITs. The goal is to have this template be pretty bare and it will be filled on based on the required task using Python and Jinja2. 

---

The foundations for create_tasks.py, get_results.py, and questions.xml are courtesy of the tutorial from AWS found at: https://blog.mturk.com/tutorial-a-beginners-guide-to-crowdsourcing-ml-training-data-with-python-and-mturk-d8df4bdf2977


Any questions please contact: edcohen@seas.upenn.edu

