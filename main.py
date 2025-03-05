# from tests.runner import test_all

# if __name__ == "__main__":
#     test_all()
    
from src.dal.database import initialize_database, db_conn

initialize_database()
    
    
 
    
    
    
# UserDAO().add_user('ilay', 'rachkovsky', 'ilay@gmail.com', '1234')
# UserDAO().get_all_users()
# UserDAO().get_user_by_id(user_id=1)
# UserDAO().delete_user_by_id(user_id=7)
# UserDAO().update_user_value_by_id(2, 'email', 'trytry@gmail.com')
