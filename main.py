# from tests.runner import test_all

# if __name__ == "__main__":
#     test_all()
    
# from src.dal.database import initialize_database

# initialize_database()
    
    
from src.dal.country_dao import CountryDAO
 
CountryDAO().get_all_countries()
# print(x)
# UserDAO().add_user('ilay', 'rachkovsky', 'ilay@gmail.com', '1234')
# UserDAO().get_all_users()
# UserDAO().get_user_by_id(user_id=1)
# UserDAO().delete_user_by_id(user_id=7)
# UserDAO().update_user_value_by_id(2, 'email', 'trytry@gmail.com')
