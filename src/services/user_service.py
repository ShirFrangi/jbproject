# built-in packages
import re

# internal packages
from src.services import errors
from src.dal.user_dao import UserDAO
from src.dal.like_dao import LikeDAO
from src.dal.vacation_dao import VacationDAO
from src.models.user_dto import User
from src.models.like_dto import Like

# external packages
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:
    def __init__(self, env: str ='prod'):
        self.env = env
        
    
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

        if UserDAO(env=self.env).email_exists(email):
            raise errors.InvalidInputError("Email already exists")
        
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=16
        )
        
        user_registered = UserDAO(env=self.env).add_user(first_name, last_name, email, hashed_password)
        return user_registered
        
    
    def login(self, email: str, password: str) -> User | None:
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
        
        if not UserDAO(env=self.env).email_exists(email):
            return None
        
        user = UserDAO(env=self.env).get_user_by_email(email)
        
        if check_password_hash(user.hashed_password, password):
            return user
    
    
    def add_like(self, user_id: int, vacation_id: int) -> Like:
        """
        Add a like for a vacation.
        """
        if not isinstance(user_id, int) or not isinstance(vacation_id, int):
            raise errors.InvalidTypeInputError("Invalid data types: user_id and vacation_id must be integer")

        if not user_id or not vacation_id:
            raise errors.MissingInputError("user_id and vacation_id are required")
        
        if UserDAO(env=self.env).get_user_by_id(user_id=user_id) == None:
            raise errors.InvalidInputError("User id not found")
        
        if VacationDAO(env=self.env).get_vacation_by_id(vacation_id=vacation_id) == None:
            raise errors.InvalidInputError("Vacation id not found")
        
        like = LikeDAO(env=self.env).add_like(user_id=user_id, vacation_id=vacation_id)
        return like


    def remove_like(self, user_id: int, vacation_id: int) -> Like:
        """
        Remove a like for a vacation.
        """
        if not isinstance(user_id, int) or not isinstance(vacation_id, int):
            raise errors.InvalidTypeInputError("Invalid data types: user_id and vacation_id must be integer")

        if not user_id or not vacation_id:
            raise errors.MissingInputError("user_id and vacation_id are required")
        
        if LikeDAO(env=self.env).get_like_by_user_and_vacation(user_id=user_id, vacation_id=vacation_id) == None:
            raise errors.InvalidInputError("Like not found")
        
        like_removed = LikeDAO(env=self.env).delete_like(user_id=user_id, vacation_id=vacation_id)
        return like_removed            
    
# 
    