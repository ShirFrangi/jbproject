
from src.services import errors
from src.dal.vacation_dao import VacationDAO
from datetime import date


class VacationService:
    
    def get_vacations(self):
        """
        This function returns all vacations sorted by start date.
        """
        vacations = VacationDAO().get_all_vacations()
        
    
    def add_vacation(self, country_id: int, vacation_info: str, vacation_start_date: tuple, vacation_end_date: tuple, price: int, photo_file_path: str):
        """
        Function to add a new vacation.
        """
        if country_id == '' or vacation_info == '' or vacation_start_date == '' or vacation_end_date == '' or price == '' or photo_file_path == '':
            raise errors.InvalidInputError("All fields are required.")
            
        if not isinstance(country_id, int) or not isinstance(vacation_info, str) or not isinstance(vacation_start_date, tuple) \
        or not isinstance(vacation_end_date, tuple) or not isinstance(price, int) or not isinstance(photo_file_path, str):
            raise errors.InvalidInputError("Invalid data types.")

        if not country_id or not vacation_info or not vacation_start_date or not vacation_end_date or not price or not photo_file_path:
            raise errors.InvalidInputError("All fields are required.")
        
        if price > 10000 or price < 0:
            raise errors.InvalidInputError("Vacation price must be greater than 0 and less than 10,000.")
        
        if date(vacation_end_date) > date(vacation_start_date):
            raise errors.InvalidInputError("The entered end date occurs before the start date.")
        
        if date(vacation_start_date) < date.today() or date(vacation_end_date) < date.today():
            raise errors.InvalidInputError(f"The start date or end date entered has occurred in the past. Please select dates starting from the current date {date.today()}")
            
        VacationDAO().add_vacation(country_id=country_id, vacation_info=vacation_info,vacation_start_date=vacation_start_date,
                                   vacation_end_date=vacation_end_date, price=price, photo_file_path=photo_file_path)
    
    
    def update_vacation(self, vacation_id:int, country_id: int, vacation_info: str, vacation_start_date: tuple, vacation_end_date: tuple, price: int, photo_file_path: str = None):
        """
        Function to update an existing vacation.
        """
        if vacation_id == '' or country_id == '' or vacation_info == '' or vacation_start_date == '' or vacation_end_date == '' or price == '':
            raise errors.InvalidInputError("All fields are required (except photo file path).")
            
        if not isinstance(vacation_id, int) or not isinstance(country_id, int) or not isinstance(vacation_info, str) or not isinstance(vacation_start_date, tuple) \
        or not isinstance(vacation_end_date, tuple) or not isinstance(price, int) or not isinstance(photo_file_path, (str, type(None))):
            raise errors.InvalidInputError("Invalid data types.")

        if not vacation_id or not country_id or not vacation_info or not vacation_start_date or not vacation_end_date or not price:
            raise errors.InvalidInputError("All fields are required (except photo file path).")
        
        if price > 10000 or price < 0:
            raise errors.InvalidInputError("Vacation price must be greater than 0 and less than 10,000.")
        
        if date(vacation_end_date) > date(vacation_start_date):
            raise errors.InvalidInputError("The entered end date occurs before the start date.")
        
        fields = [("country_id", country_id), ("vacation_info", vacation_info), ("vacation_start_date", vacation_start_date),
                  ("vacation_end_date", vacation_end_date),("price", price),("photo_file_path", photo_file_path)]
        
        for field_name, value in fields:
            VacationDAO().update_vacation_value_by_id(vacation_id=vacation_id, column_to_update=field_name, new_value=value)
    
    
    def delete_vacation(self, vacation_id):
        """
        Function to delete an existing vacation.
        """
        if vacation_id == '':
            raise errors.InvalidInputError("All fields are required.")
            
        if not isinstance(vacation_id, int):
            raise errors.InvalidInputError("Invalid data types.")

        if not vacation_id:
            raise errors.InvalidInputError("All fields are required.")
        VacationDAO().delete_vacation_by_id(vacation_id=vacation_id)
    
# 
          