# internal packages
from tests.test_user_service import TestUserService
from tests.test_vacation_service import TestVacationService
from tests.runner import test_all


if __name__ == "__main__":
    test_all()

# 

# """
# TODO:
# 1. in user service i did try except with raise exception in try block - fix it.
# 2. delete the print items
# """
