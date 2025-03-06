# built-in packages
from typing import List
from datetime import date

# internal packages
from src.dal.database import db_conn
from src.models.vacation import Vacation

# external packages 
from psycopg.sql import SQL, Identifier, Placeholder
import psycopg.rows as pgrows


class VacationDAO:
    def __init__(self):
        self.table_name = "vacations"


    def get_all_vacations(self) -> List[Vacation]:
        """
        Retrieves all vacations from the 'vacations' table.
        Returns: List[Vacation]: A list of Vacation objects.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} order by {};").format(Identifier(self.table_name), Identifier("vacation_start_date"))
            cur.execute(query)
            result = cur.fetchall()
            
        return [Vacation(vacation_id=row['vacation_id'], country_id=row['country_id'], vacation_info=row['vacation_info'],
                         vacation_start_date=row['vacation_start_date'], vacation_end_date=row['vacation_end_date'], price=row['price'],
                         photo_file_path=row['photo_file_path']) for row in result]


    def add_vacation(self, country_id: int, vacation_info: str, vacation_start_date: date, vacation_end_date: date, price: int, photo_file_path: str) -> Vacation:
        """
        Add a new vacation to the 'vacations' table with the provided details.
        Args: country_id (int), vacation_info (str), vacation_start_date (date), vacation_end_date (date), price (int), photo_file_path (str).
        Returns: Vacation: The inserted vacation as a Vacation object.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(
                Identifier(self.table_name),  
                SQL(", ").join(map(Identifier, ["country_id", "vacation_info", "vacation_start_date", "vacation_end_date", "price", "photo_file_path"])),
                SQL(", ").join(Placeholder() for _ in range(6)))
            cur.execute(query, (country_id, vacation_info, vacation_start_date, vacation_end_date, price, photo_file_path)) 
            db_conn.commit()
            result = cur.fetchone()
            
        return Vacation(vacation_id=result['vacation_id'], country_id=result['country_id'], vacation_info=result['vacation_info'],
                        vacation_start_date=result['vacation_start_date'], vacation_end_date=result['vacation_end_date'], 
                        price=result['price'], photo_file_path=result['photo_file_path'])
        
                
    def get_vacation_by_id(self, vacation_id: int) -> Vacation | None:
        """
        Retrieves a vacation from the 'vacations' table by vacation_id.
        Args: vacation_id (int)
        Returns: Vacation: The vacation object with the specified vacation_id, or None if not found.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("vacation_id"), Placeholder())
            cur.execute(query, (vacation_id,))
            result = cur.fetchall()
            
        if result:
            row = result[0]  
            return Vacation(vacation_id=row['vacation_id'], country_id=row['country_id'], vacation_info=row['vacation_info'],
                            vacation_start_date=row['vacation_start_date'], vacation_end_date=row['vacation_end_date'],
                            price=row['price'], photo_file_path=row['photo_file_path'])
        else:
            return None
   
        
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
