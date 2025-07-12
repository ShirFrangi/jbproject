# John Bryce project - Shir Frangi
This is the code for John Bryce Full Stack Python Project


## Running the Project for the First Time
When running the project for the first time, the following queries must be executed:
    """
    CREATE DATABASE jbproject_prod;
    CREATE DATABASE jbproject_dev;
    """

## Default Setup
By default, the application and tests run using the development (dev) environment. This means they connect to development resources and databases, keeping production data safe.

## Switching to Production
If you want to run the application or tests against the production (prod) environment, you need to update the environment settings in the config.py file. For example:

test_env = 'prod'
display_env = 'prod'
