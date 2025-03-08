# built-in packages
import unittest

# internal packages
from tests.test_user_service import TestUserService
from tests.test_vacation_service import TestVacationService


def test_all():
    test_cases = [TestUserService, TestVacationService]
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    for test_class in test_cases:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    result = unittest.TextTestRunner().run(suite)
    return result.wasSuccessful()

# 
