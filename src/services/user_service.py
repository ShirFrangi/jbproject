# built-in packages
import re

# internal packages
from src.services import errors
from src.dal.user_dao import UserDAO
from src.dal.like_dao import LikeDAO
from models.user import User

class UserService:
    def register(self, first_name, last_name, email, password):
        """
        Registers a new user by validating the input fields and saving the user to the DB.
        """
        if first_name == '' or last_name == '' or email == '' or password == '':
            raise errors.InvalidInputError("All fields are required")
            
        if not isinstance(first_name, str) or not isinstance(last_name, str) or not isinstance(email, str) or not isinstance(password, str):
            raise errors.InvalidInputError("Invalid data types: email and password must be strings, role must be a Role enum")

        if not first_name or not last_name or not email or not password:
            raise errors.InvalidInputError("All fields are required")

        if not bool(re.match(r"[^@]+@[^@]+\.[^@]+", email)):
            raise errors.InvalidInputError("Invalid email format")

        if len(password) < 4:
            raise errors.InvalidInputError("Password must be at least 4 characters long")

        if UserDAO().email_exists(email):
            raise errors.InvalidInputError("Email already exists")
        
        user = User(user_id=None, first_name=first_name, last_name=last_name, email=email, password=password)
        UserDAO().add_user(user)
        print(f"User {email} registered successfully")
        
    
    def login(self, email: str, password: str):
        """
        Authenticates a user by email and password. Returns the user object if login is successful.
        """
        if not isinstance(email, str) or not isinstance(password, str):
            raise errors.InvalidInputError("Email and password must be strings")

        if not email or not password:
            raise errors.InvalidInputError("Email and password are required")
        
        if email == '' or password == '':
            raise errors.InvalidInputError("Invalid value provided for email or password")
        
        if not bool(re.match(r"[^@]+@[^@]+\.[^@]+", email)):
            raise errors.InvalidInputError("Invalid email format")
        
        if len(password) < 4:
            raise errors.InvalidInputError("Password must be at least 4 characters long")
        
        if not UserDAO().email_exists(email):
            raise errors.InvalidInputError("User not found")
        
        if UserDAO().get_user_by_email_and_password(email, password) == None:
            raise errors.InvalidInputError("Incorrect email or password")
            
        print(f"User {email} logged in successfully")
        return UserDAO().get_user_by_email_and_password(email, password)
    
    
    def add_like(self, user_id, vacation_id):
        """
        Adds a like for a vacation.
        """
        if not isinstance(user_id, int) or not isinstance(vacation_id, int):
            raise errors.InvalidInputError("Invalid data types: user_id and vacation_id must be integer")

        if not user_id or not vacation_id:
            raise errors.InvalidInputError("user_id and vacation_id are required")
        
        LikeDAO().add_like(user_id=user_id, vacation_id=vacation_id)
        print(f"User {user_id} liked vacation {vacation_id}")


    def remove_like(self, user_id, vacation_id):
        """
        Remove a like for a vacation.
        """
        if not isinstance(user_id, int) or not isinstance(vacation_id, int):
            raise errors.InvalidInputError("Invalid data types: user_id and vacation_id must be integer")

        if not user_id or not vacation_id:
            raise errors.InvalidInputError("user_id and vacation_id are required")
        
        LikeDAO().delete_like(user_id=user_id, vacation_id=vacation_id)
        print(f"User {user_id} unliked vacation {vacation_id}")
    
# 
    