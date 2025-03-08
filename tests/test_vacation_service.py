# built-in packages
import unittest
from datetime import date, timedelta

# internal packages
from src.services.vacation_service import VacationService
from src.dal.vacation_dao import VacationDAO
from src.dal.database import initialize_database
from src.services import errors
from src.models.vacation_dto import Vacation


class TestVacationService(unittest.TestCase):
    def setUp(self):
        self.vacation_service = VacationService(env='dev')
        initialize_database(env='dev')  

       
    # ---Tests for get vacations function---
    def test_get_vacations_success(self):
        """
        Positive test: get all vacations.
        """
        vacations = self.vacation_service.get_vacations()
        self.assertIsInstance(vacations, list)
        self.assertGreater(len(vacations), 0)
        
    
    def test_get_vacations_failed(self):
        """
        Negative test: empty vacation list.
        """
        VacationDAO(env='dev').delete_all_vacations()
        with self.assertRaises(Exception) as context:
            self.vacation_service.get_vacations()
        self.assertEqual(str(context.exception), "No vacations found.")
    
    
    # ---Tests for add vacation function---
    def test_add_vacation_success(self):
        """
        Positive test: add vacation.
        """
        vacation = self.vacation_service.add_vacation(
            country_id=1, 
            vacation_info="Test Vacation", 
            vacation_start_date=date(2025, 5, 1),
            vacation_end_date=date(2025, 5, 10),
            price=5000, 
            photo_file_path="path/to/photo.jpg"
        )
        self.assertIsInstance(vacation, Vacation)
        self.assertEqual(vacation.vacation_info, "Test Vacation")
        
    
    def test_add_vacation_missing_fields(self):
        """
        Negative test: add vacation with missing fields.
        """
        with self.assertRaises(errors.InvalidInputError):
            self.vacation_service.add_vacation(
                country_id=1, 
                vacation_info="", 
                vacation_start_date=date(2025, 5, 1),
                vacation_end_date=date(2025, 5, 10),
                price=5000, 
                photo_file_path="path/to/photo.jpg"
            )
        
    
    def test_add_vacation_price_greater_than_10000(self):
        """
        Negative test: add vacation with price greater than 10000.
        """
        with self.assertRaises(errors.InvalidInputError) as context:
            self.vacation_service.add_vacation(
                country_id=2, 
                vacation_info="vacation info", 
                vacation_start_date=date(2025, 5, 1),
                vacation_end_date=date(2025, 5, 10),
                price=10500, 
                photo_file_path="path/to/photo.jpg"
            )
        self.assertEqual(str(context.exception), "Vacation price must be greater than 0 and less than 10,000.")
        
        
    def test_add_vacation_price_less_than_0(self):
        """
        Negative test: add vacation with price less than 0.
        """
        with self.assertRaises(errors.InvalidInputError) as context:
            self.vacation_service.add_vacation(
                country_id=2, 
                vacation_info="vacation info", 
                vacation_start_date=date(2025, 5, 1),
                vacation_end_date=date(2025, 5, 10),
                price=-600, 
                photo_file_path="path/to/photo.jpg"
            )
        self.assertEqual(str(context.exception), "Vacation price must be greater than 0 and less than 10,000.")
        
    
    def test_add_vacation_end_date_before_start_date(self):
        """
        Negative test: add vacation with end date occurs before start date.
        """
        with self.assertRaises(errors.InvalidInputError) as context:
            self.vacation_service.add_vacation(
                country_id=2, 
                vacation_info="vacation info", 
                vacation_start_date=date(2025, 5, 10),
                vacation_end_date=date(2025, 5, 5),
                price=1600, 
                photo_file_path="path/to/photo.jpg"
            )
        self.assertEqual(str(context.exception), "The entered end date occurs before the start date.")
        
        
    def test_add_vacation_end_date_before_today(self):
        """
        Negative test: add vacation with end date occurs before today.
        """
        with self.assertRaises(errors.InvalidInputError) as context:
            self.vacation_service.add_vacation(
                country_id=5, 
                vacation_info="vacation info", 
                vacation_start_date=date.today()- timedelta(days=10),
                vacation_end_date=date.today()- timedelta(days=5),
                price=1600, 
                photo_file_path="path/to/photo.jpg"
            )
        self.assertEqual(str(context.exception), f"The start date or end date entered has occurred in the past. Please select dates starting from the current date {date.today()}")

       
    def test_add_vacation_invalid_country_id(self):
        """
        Negative test: add vacation with country id dose not exist.
        """
        with self.assertRaises(errors.InvalidInputError) as context:
            self.vacation_service.add_vacation(
                country_id=9999, 
                vacation_info="vacation info", 
                vacation_start_date=date(2025, 9, 3),
                vacation_end_date=date(2025, 9, 10),
                price=1600, 
                photo_file_path="path/to/photo.jpg"
            )
        self.assertEqual(str(context.exception), "Country id not found.")
        
        
    # ---Tests for update vacation function---
    def test_update_vacation_success(self):
        """
        Positive test: update vacation.
        """
        vacation = self.vacation_service.update_vacation(
            vacation_id=1, 
            country_id=1, 
            vacation_info="Updated Vacation", 
            vacation_start_date=date(2025, 6, 1),
            vacation_end_date=date(2025, 6, 10),
            price=3000, 
            photo_file_path="new/photo/path.jpg"
        )
        self.assertEqual(vacation.vacation_info, "Updated Vacation")
        
        
    def test_update_vacation_invalid_id(self):
        """
        Negative test: update vacation with country id dose not exist.
        """
        with self.assertRaises(errors.InvalidInputError) as context:
            self.vacation_service.update_vacation(
                vacation_id=9999, 
                country_id=1, 
                vacation_info="Updated Vacation", 
                vacation_start_date=date(2025, 6, 1),
                vacation_end_date=date(2025, 6, 10),
                price=3000, 
                photo_file_path="new/photo/path.jpg"
            )
        self.assertEqual(str(context.exception), "Vacation id not found.")
        
        
    def test_update_vacation_price_greater_than_10000(self):
        """
        Negative test: update vacation with price greater than 10000.
        """
        with self.assertRaises(errors.InvalidInputError) as context:
            self.vacation_service.update_vacation(
                vacation_id=3,
                country_id=2, 
                vacation_info="vacation info", 
                vacation_start_date=date(2025, 5, 1),
                vacation_end_date=date(2025, 5, 10),
                price=10500, 
                photo_file_path="path/to/photo.jpg"
            )
        self.assertEqual(str(context.exception), "Vacation price must be greater than 0 and less than 10,000.")
        
        
    def test_update_vacation_price_less_than_0(self):
        """
        Negative test: update vacation with price less than 0.
        """
        with self.assertRaises(errors.InvalidInputError) as context:
            self.vacation_service.update_vacation(
                vacation_id=4,
                country_id=2, 
                vacation_info="vacation info", 
                vacation_start_date=date(2025, 5, 1),
                vacation_end_date=date(2025, 5, 10),
                price=-600, 
                photo_file_path="path/to/photo.jpg"
            )
        self.assertEqual(str(context.exception), "Vacation price must be greater than 0 and less than 10,000.")
        

    def test_update_vacation_end_date_before_start_date(self):
        """
        Negative test: update vacation with end date occurs before start date.
        """
        with self.assertRaises(errors.InvalidInputError) as context:
            self.vacation_service.update_vacation(
                vacation_id=4,
                country_id=2, 
                vacation_info="vacation info", 
                vacation_start_date=date(2025, 5, 10),
                vacation_end_date=date(2025, 5, 5),
                price=1600, 
                photo_file_path="path/to/photo.jpg"
            )
        self.assertEqual(str(context.exception), "The entered end date occurs before the start date.")
    
    
    def test_update_vacation_invalid_country_id(self):
        """
        Negative test: update vacation with country id dose not exist.
        """
        with self.assertRaises(errors.InvalidInputError) as context:
            self.vacation_service.update_vacation(
                vacation_id=3,
                country_id=9999, 
                vacation_info="vacation info", 
                vacation_start_date=date(2025, 9, 3),
                vacation_end_date=date(2025, 9, 10),
                price=1600, 
                photo_file_path="path/to/photo.jpg"
            )
        self.assertEqual(str(context.exception), "Country id not found.")
        

    # ---Tests for update vacation function---
    def test_delete_vacation_success(self):
        """
        Positive test: delete vacation.
        """
        vacation = self.vacation_service.delete_vacation(vacation_id=1)
        self.assertIsInstance(vacation, Vacation)
        
    
    def test_delete_vacation_invalid_id(self):
        """
        Negative test: delete vacation with country id dose not exist.
        """
        with self.assertRaises(errors.InvalidInputError) as context:
            self.vacation_service.delete_vacation(vacation_id=9999)
        self.assertEqual(str(context.exception), "Vacation id not found.") 
 
# 
