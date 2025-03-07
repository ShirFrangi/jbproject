# built-in packages
import unittest

# internal packages
from src.services.user_service import UserService
from src.dal.database import initialize_database
from src.services import errors
from src.models.user_dto import User
from src.models.like_dto import Like


class TestVacationService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService(env='dev')
        initialize_database(env='dev')  
        
        
    # ---Tests for register function---
    def test_register_success(self):
        """
        Positive test: new user registration.
        """
        user = self.user_service.register('John', 'Doe', 'john@example.com', 'password1234')
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'john@example.com')
    
    
    def test_register_invalid_email(self):
        """
        Negative test: invalid email.
        """
        with self.assertRaises(errors.InvalidInputError):
            self.user_service.register('John', 'Doe', 'johnexample.com', 'password1234')
            
    
    def test_register_invalid_password(self):
        """
        Negative test: invalid password.
        """
        with self.assertRaises(errors.InvalidInputError):
            self.user_service.register('John', 'Doe', 'john@example.com', 'pas')
            
            
    def test_register_email_exist(self):
        """
        Negative test: email exist.
        """
        with self.assertRaises(errors.InvalidInputError):
            self.user_service.register('John', 'Doe', 'test@gmail.com', 'password1234')
            
    
    # ---Tests for login function---    
    def test_login_success(self):
        """
        Positive test: user login.
        """
        user = self.user_service.login('shir@gmail.com', '1234')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'shir@gmail.com')


    def test_login_invalid_credentials(self):
        """
        Negative test: incorrect login credentials.
        """
        with self.assertRaises(errors.InvalidInputError):
            self.user_service.login('shir@gmail.com', 'wrongpassword')
    
            
    def test_login_invalid_email(self):
        """
        Negative test: invalid email.
        """
        with self.assertRaises(errors.InvalidInputError):
            self.user_service.login('shir-gmail.com', '1234')
            
            
    def test_login_invalid_password(self):
        """
        Negative test: invalid password.
        """
        with self.assertRaises(errors.InvalidInputError):
            self.user_service.login('shir@gmail.com', '123')
            
            
    def test_login_user_not_exist(self):
        """
        Negative test: user does not exist.
        """
        with self.assertRaises(errors.InvalidInputError):
            self.user_service.login('david@gmail.com', '1234')
            
    
    # ---Tests for add like function---  
    def test_add_like_success(self):
        """
        Positive test: add like.
        """
        like = self.user_service.add_like(1, 1) 
        self.assertIsNotNone(like)
        self.assertIsInstance(like, Like)
        self.assertEqual(like.user_id, 1)
        self.assertEqual(like.vacation_id, 1)


    def test_add_like_invalid_user(self):
        """
        Negative test: user does not exist.
        """
        with self.assertRaises(errors.InvalidInputError):
            self.user_service.add_like(9999, 1)
            
    
    def test_add_like_invalid_vacation(self):
        """
        Negative test: user does not exist.
        """
        with self.assertRaises(errors.InvalidInputError):
            self.user_service.add_like(1, 9999)
            
    
    # ---Tests for remove like function---
    def test_remove_like_success(self):
        """
        Positive test: remove like.
        """
        like = self.user_service.add_like(1, 1)
        self.assertIsNotNone(like) 
        result = self.user_service.remove_like(1, 1)
        self.assertEqual(result, "Like removed successfully")


    def test_remove_like_invalid_like(self):
        """
        Negative test: like does not exist.
        """
        with self.assertRaises(errors.InvalidInputError):
            self.user_service.remove_like(1, 9999)
            
    
    def test_remove_like_invalid_user_type(self):
        """
        Negative test: user_id as string.
        """
        like = self.user_service.add_like(1, 1)
        self.assertIsNotNone(like) 
        with self.assertRaises(errors.InvalidInputError):
            self.user_service.remove_like("1", 1)
     
            
    def test_remove_like_invalid_vacation_type(self):
        """
        Negative test: vacation_id as string.
        """
        like = self.user_service.add_like(1, 1)
        self.assertIsNotNone(like)
        with self.assertRaises(errors.InvalidInputError):
            self.user_service.remove_like(1, "1")   
      
# 
