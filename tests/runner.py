from unittest import TestSuite, TestLoader, TestResult

from tests.test_user_service import TestUserService
from tests.test_vacation_service import TestVacationService

def test_all():
    test_cases = (TestUserService, TestVacationService)
    suite = TestSuite()
    loader = TestLoader()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTest(tests)
    
    result = TestResult()
    suite.run(result=result)