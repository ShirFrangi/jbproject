# John Bryce project - Shir Frangi
This is the code for John Bryce Full Stack Python Project


## Default Setup:

By default, the application and tests run using the development (dev) environment. This means they connect to development resources and databases, keeping production data safe.


## Switching to Production:

If you want to run the application or tests against the production (prod) environment, you need to update the environment settings in the config.py file. For example:

test_env = 'prod'
display_env = 'prod'

Important:
Make sure that test_env and display_env are set to the same environment.


## Before Running the Project:

1. make sure the relevant databases ('jbproject_prod', 'jbproject_dev') exist on your system.  
If they do not exist, the following queries must be executed:
"""
CREATE DATABASE jbproject_prod;
CREATE DATABASE jbproject_dev;
"""
2. Install all the required packages for the project by running:
On Windows: pip install -r requirements.txt
On Mac / Linux: pip3 install -r requirements.txt


## Running the Project:

To run the project — both the tests and the application — you need to execute the main.py file located in the root folder of the project.
After that, to view the web application in Chrome, enter the following URL in the address bar: http://127.0.0.1:5001/

Important:
If port 5001 is already in use on your machine, you should either run the application on another available port (and update the port in the main.py file accordingly) or terminate the existing process that is using this port.