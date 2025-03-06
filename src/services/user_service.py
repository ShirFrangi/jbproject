# built-in packages
import re

# internal packages
from src.services import errors
from src.dal.user_dao import UserDAO
from src.dal.like_dao import LikeDAO
from src.dal.vacation_dao import VacationDAO
from src.models.user import User
from src.models.like import Like


class UserService:
    def register(self, first_name: str, last_name: str, email: str, password: str) -> User:
        """
        Registers a new user by validating the input fields and saving the user to the DB.
        """
        if first_name == '' or last_name == '' or email == '' or password == '':
            raise errors.InvalidInputError("All fields are required")
            
        if not isinstance(first_name, str) or not isinstance(last_name, str) or not isinstance(email, str) or not isinstance(password, str):
            raise errors.InvalidTypeInputError("Invalid data types: email and password must be strings, role must be a Role enum")

        if not first_name or not last_name or not email or not password:
            raise errors.MissingInputError("All fields are required")

        if not bool(re.match(r"[^@]+@[^@]+\.[^@]+", email)):
            raise errors.InvalidInputError("Invalid email format")

        if len(password) < 4:
            raise errors.InvalidInputError("Password must be at least 4 characters long")

        if UserDAO().email_exists(email):
            raise errors.InvalidInputError("Email already exists")
        
        try:
            user_registered = UserDAO().add_user(first_name, last_name, email, password)
            print(f"User with email {email} registered successfully")
            return user_registered
        
        except Exception as e:
            print(f"An unexpected error occurred while registering the user: {e}")
        
    
    def login(self, email: str, password: str) -> User:
        """
        Authenticates a user by email and password. Returns the user object if login is successful.
        """
        if email == '' or password == '':
            raise errors.InvalidInputError("Invalid value provided for email or password")
        
        if not isinstance(email, str) or not isinstance(password, str):
            raise errors.InvalidTypeInputError("Email and password must be strings")

        if not email or not password:
            raise errors.MissingInputError("Email and password are required")
        
        if not bool(re.match(r"[^@]+@[^@]+\.[^@]+", email)):
            raise errors.InvalidInputError("Invalid email format")
        
        if len(password) < 4:
            raise errors.InvalidInputError("Password must be at least 4 characters long")
        
        if not UserDAO().email_exists(email):
            raise errors.InvalidInputError("User not found")
        
        try:
            user_logged_in = UserDAO().get_user_by_email_and_password(email, password)
        
            if  user_logged_in == None:
                raise errors.InvalidInputError("Incorrect email or password")
            
            else:
                print(f"User {email} logged in successfully")
                return user_logged_in
        
        except Exception as e:
            print(f"An unexpected error occurred while logging the user: {e}")
    
    
    def add_like(self, user_id: int, vacation_id: int) -> Like:
        """
        Add a like for a vacation.
        """
        if not isinstance(user_id, int) or not isinstance(vacation_id, int):
            raise errors.InvalidTypeInputError("Invalid data types: user_id and vacation_id must be integer")

        if not user_id or not vacation_id:
            raise errors.MissingInputError("user_id and vacation_id are required")
        
        if UserDAO().get_user_by_id(user_id=user_id) == None:
            raise errors.InvalidInputError("User id not found")
        
        if VacationDAO().get_vacation_by_id(vacation_id=vacation_id) == None:
            raise errors.InvalidInputError("Vacation id not found")
            
        try:
            like = LikeDAO().add_like(user_id=user_id, vacation_id=vacation_id)
            print(f"User {user_id} liked vacation {vacation_id}")
            return like
        
        except Exception as e:
            print(f"An unexpected error occurred while adding a like: {e}")


    def remove_like(self, user_id: int, vacation_id: int) -> str:
        """
        Remove a like for a vacation.
        """
        if not isinstance(user_id, int) or not isinstance(vacation_id, int):
            raise errors.InvalidTypeInputError("Invalid data types: user_id and vacation_id must be integer")

        if not user_id or not vacation_id:
            raise errors.MissingInputError("user_id and vacation_id are required")
        
        if LikeDAO().get_like_by_user_and_vacation(user_id=user_id, vacation_id=vacation_id) == None:
            raise errors.InvalidInputError("Like not found")
        
        try:
            like_removed = LikeDAO().delete_like(user_id=user_id, vacation_id=vacation_id)
            return like_removed
        
        except Exception as e:
            print(f"An unexpected error occurred while remove a like: {e}")
            
    
# 
    