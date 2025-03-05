# built-in packages
from typing import List, Optional
from datetime import date

# internal packages
from src.dal.database import db_conn

# external packages 
from psycopg.sql import SQL, Identifier, Placeholder
import psycopg.rows as pgrows


class VacationDAO:
    def __init__(self):
        self.table_name = "vacations"


    def get_all_vacations(self) -> List[dict]:
        """
        Retrieves all vacations from the 'vacations' table.
        Returns: List[dict]: A list of dictionaries representing the vacations in the table. Each dictionary contains column-value pairs for a vacation.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {};").format(Identifier(self.table_name))
            cur.execute(query)
            result = cur.fetchall()
            
        return result


    def add_vacation(self, country_id: int, vacation_info: str, vacation_start_date: tuple, vacation_end_date: tuple, price: str, photo_file_path: str) -> dict:
        """
        Add a new vacation to the 'vacations' table with the provided details.
        Args: country_id (int), vacation_info (str), vacation_start_date (tuple), vacation_end_date (tuple), price (str), photo_file_path (str).
        Returns: dict: A dictionary representing the inserted vacation, including all columns and their values.
        """
        vacation_start_date = date(vacation_start_date)
        vacation_end_date = date(vacation_end_date)
        
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(
                Identifier(self.table_name),  
                SQL(", ").join(map(Identifier, ["country_id", "vacation_info", "vacation_start_date", "vacation_end_date", "price", "photo_file_path"])),
                SQL(", ").join(Placeholder() for _ in range(6)))
            cur.execute(query, (country_id, vacation_info, vacation_start_date, vacation_end_date, price, photo_file_path)) 
            db_conn.commit()
            result = cur.fetchone()
            
        return result
        
                
    def get_vacation_by_id(self, vacation_id: int) -> Optional[dict]:
        """
        Retrieves a vacation from the 'vacations' table by vacation_id.
        Args: vacation_id (int)
        Returns: dict: A dictionary representing the vacation with the specified vacation_id, or None if no vacation is found.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("vacation_id"), Placeholder())
            cur.execute(query, (vacation_id,))
            result = cur.fetchall()
            
        return result
   
        
    def update_vacation_value_by_id(self, vacation_id: int, column_to_update: str, new_value: str) -> str:
        """
        Updates the value of a specific column for a vacation in the 'vacations' table.
        Args: vacation_id (int), column_to_update (str), new_value (str).
        Returns: str: A message indicating whether the update was successful.
        """
        with db_conn.cursor() as cur:
            query = SQL("UPDATE {} SET {} = {} WHERE {} = {}").format(
                Identifier(self.table_name), Identifier(column_to_update), Placeholder(), Identifier("vacation_id"),Placeholder())
            cur.execute(query, (new_value, vacation_id))
            db_conn.commit()
            
            return f"Updated vacation with vacation_id {vacation_id}." if cur.rowcount == 1 else f"Update vacation with vacation_id {vacation_id} failed."
        
        
    def delete_vacation_by_id(self, vacation_id: int) -> str:
        """
        Deletes a vacation from the 'vacations' table by vacation_id.
        Args: vacation_id (int)
        Returns: str: A message indicating whether the deletion was successful.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("DELETE FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("vacation_id"), Placeholder())
            cur.execute(query, (vacation_id,))
            db_conn.commit()

            return f"Deleted vacation with vacation_id {vacation_id}." if cur.rowcount == 1 else f"Deletion vacation with vacation_id {vacation_id} failed."

# 
