from datetime import date

class Vacation:
    def __init__(self, vacation_id: int, country_id: int, vacation_info: str, vacation_start_date: date, vacation_end_date: date, price: int, photo_file_path: str):
        self.vacation_id = vacation_id
        self.country_id = country_id
        self.vacation_info = vacation_info
        self.vacation_start_date = vacation_start_date
        self.vacation_end_date = vacation_end_date
        self.price = price
        self.photo_file_path = photo_file_path
    
    def __repr__(self):
        return f"Vacation(vacation_id={self.vacation_id}, country_id={self.country_id}, vacation_info='{self.vacation_info}',
                vacation_start_date='{self.vacation_start_date}', vacation_end_date='{self.vacation_end_date}', price={self.price},
                photo_file_path='{self.photo_file_path}')"


# 
