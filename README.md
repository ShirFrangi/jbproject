# jbproject
This is the code for John Bryce Full Stack  Python Project

## Comments
Currently, the tests are testing a DEV environment. To test a PROD environment, you must change the "setUp" method in each test. For example:

def setUp(self):
        self.user_service = UserService(env='prod')
        initialize_database(env='prod') 