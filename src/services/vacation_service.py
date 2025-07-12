# built-in packages
from datetime import date
from typing import List

# internal packages
from src.services import errors
from src.dal.vacation_dao import VacationDAO
from src.dal.country_dao import CountryDAO
from src.models.vacation_dto import Vacation


class VacationService:
    def __init__(self, env: str ='prod'):
        self.env = env
        
    def get_vacations(self) -> List[Vacation]:
        """
        This function returns all vacations sorted by start date.
        """
        vacations = VacationDAO(env=self.env).get_all_vacations()
        if vacations == []:
            raise Exception("No vacations found.")
        else:
            return vacations
        
    
    def add_vacation(self, country_id: int, vacation_info: str, vacation_start_date: date, vacation_end_date: date, price: int, photo_file_path: str) -> Vacation:
        """
        Function to add a new vacation.
        """
        if country_id == '' or vacation_info == '' or vacation_start_date == '' or vacation_end_date == '' or price == '' or photo_file_path == '':
            raise errors.InvalidInputError("All fields are required.")
            
        if not isinstance(country_id, int) or not isinstance(vacation_info, str) or not isinstance(vacation_start_date, date) \
        or not isinstance(vacation_end_date, date) or not isinstance(price, int) or not isinstance(photo_file_path, str):
            raise errors.InvalidTypeInputError("Invalid data types.")

        if not country_id or not vacation_info or not vacation_start_date or not vacation_end_date or not price or not photo_file_path:
            raise errors.MissingInputError("All fields are required.")
        
        if price > 10000 or price < 0:
            raise errors.InvalidInputError("Vacation price must be greater than 0 and less than 10,000.")
        
        if vacation_end_date < vacation_start_date:
            raise errors.InvalidInputError("The entered end date occurs before the start date.")
        
        if vacation_start_date < date.today() or vacation_end_date < date.today():
            raise errors.InvalidInputError(f"The start date or end date entered has occurred in the past. Please select dates starting from the current date {date.today()}")
        
        if CountryDAO(env=self.env).get_country_by_id(country_id=country_id) == None:
            raise errors.InvalidInputError("Country id not found.")
        
        vacation_added = VacationDAO(env=self.env).add_vacation(country_id=country_id, vacation_info=vacation_info,vacation_start_date=vacation_start_date,
                                vacation_end_date=vacation_end_date, price=price, photo_file_path=photo_file_path)

        return vacation_added
        
    
    def update_vacation(self, vacation_id:int, country_id: int, vacation_info: str, vacation_start_date: date, vacation_end_date: date, price: int, photo_file_path: str = None) -> Vacation:
        """
        Function to update an existing vacation.
        """
        if vacation_id == '' or country_id == '' or vacation_info == '' or vacation_start_date == '' or vacation_end_date == '' or price == '':
            raise errors.InvalidInputError("All fields are required (except photo file path).")
            
        if not isinstance(vacation_id, int) or not isinstance(country_id, int) or not isinstance(vacation_info, str) or not isinstance(vacation_start_date, date) \
        or not isinstance(vacation_end_date, date) or not isinstance(price, int) or not isinstance(photo_file_path, (str, type(None))):
            raise errors.InvalidTypeInputError("Invalid data types.")

        if not vacation_id or not country_id or not vacation_info or not vacation_start_date or not vacation_end_date or not price:
            raise errors.MissingInputError("All fields are required (except photo file path).")
        
        if price > 10000 or price < 0:
            raise errors.InvalidInputError("Vacation price must be greater than 0 and less than 10,000.")
        
        if vacation_end_date < vacation_start_date:
            raise errors.InvalidInputError("The entered end date occurs before the start date.")
        
        if VacationDAO(env=self.env).get_vacation_by_id(vacation_id=vacation_id) == None:
            raise errors.InvalidInputError("Vacation id not found.")
        
        if CountryDAO(env=self.env).get_country_by_id(country_id=country_id) == None:
            raise errors.InvalidInputError("Country id not found.")
        
        fields = [("country_id", country_id), ("vacation_info", vacation_info), ("vacation_start_date", vacation_start_date),
                  ("vacation_end_date", vacation_end_date),("price", price),("photo_file_path", photo_file_path)]
            
        for field_name, value in fields:
            VacationDAO(env=self.env).update_vacation_value_by_id(vacation_id=vacation_id, column_to_update=field_name, new_value=value)
            
        vacation_updated = Vacation(vacation_id=vacation_id, country_id=country_id, vacation_info=vacation_info, vacation_start_date=vacation_start_date,
                                     vacation_end_date=vacation_end_date, price=price, photo_file_path=photo_file_path)

        return vacation_updated
            
    
    def delete_vacation(self, vacation_id: int) -> Vacation:
        """
        Function to delete an existing vacation.
        """ 
        if not isinstance(vacation_id, int):
            raise errors.InvalidTypeInputError("Invalid data types.")

        if not vacation_id:
            raise errors.MissingInputError("All fields are required.")
        
        if VacationDAO(env=self.env).get_vacation_by_id(vacation_id=vacation_id) == None:
            raise errors.InvalidInputError("Vacation id not found.")
        
        vacation_deleted = VacationDAO(env=self.env).delete_vacation_by_id(vacation_id=vacation_id)
        return vacation_deleted
    
# 
          