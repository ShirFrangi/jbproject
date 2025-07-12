# built-in packages
from typing import List
from datetime import date

# internal packages
from src.dal.database import dev_db_conn, prod_db_conn
from src.models.vacation_dto import Vacation

# external packages 
from psycopg.sql import SQL, Identifier, Placeholder
import psycopg.rows as pgrows


class VacationDAO:
    def __init__(self, env: str ='prod'):
        self.table_name = "vacations"
        self.db_conn = prod_db_conn if env == 'prod' else dev_db_conn


    def get_all_vacations(self) -> List[Vacation]:
        """
        Retrieves all vacations from the 'vacations' table.
        Returns: List[Vacation]: A list of Vacation objects.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("""SELECT *, (SELECT COUNT(*) FROM {} AS l WHERE l.{} = v.{}) AS likes_count
                            FROM {} AS v JOIN {} AS c ON v.{} = c.{} ORDER BY {};"""
                            ).format(Identifier("likes"),
                                     Identifier("vacation_id"),
                                     Identifier("vacation_id"),
                                     Identifier(self.table_name),
                                     Identifier("countries"),
                                     Identifier("country_id"),
                                     Identifier("country_id"),
                                     Identifier("vacation_start_date"))
            cur.execute(query)
            result = cur.fetchall()
            
        return [Vacation(vacation_id=row['vacation_id'], country_id=row['country_id'], country_name=row['country_name'], vacation_info=row['vacation_info'],
                         vacation_start_date=row['vacation_start_date'], vacation_end_date=row['vacation_end_date'], price=row['price'],
                         photo_file_path=row['photo_file_path'], likes_count=row['likes_count']) for row in result]


    def add_vacation(self, country_id: int, vacation_info: str, vacation_start_date: date, vacation_end_date: date, price: int, photo_file_path: str) -> Vacation:
        """
        Add a new vacation to the 'vacations' table with the provided details.
        Args: country_id (int), vacation_info (str), vacation_start_date (date), vacation_end_date (date), price (int), photo_file_path (str).
        Returns: Vacation: The inserted vacation as a Vacation object.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(
                Identifier(self.table_name),  
                SQL(", ").join(map(Identifier, ["country_id", "vacation_info", "vacation_start_date", "vacation_end_date", "price", "photo_file_path"])),
                SQL(", ").join(Placeholder() for _ in range(6)))
            cur.execute(query, (country_id, vacation_info, vacation_start_date, vacation_end_date, price, photo_file_path)) 
            self.db_conn.commit()
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
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("""SELECT * 
                        FROM {} as v
                        JOIN {} as c
                        ON  v.country_id = c.country_id
                        WHERE {} = {}""").format(Identifier(self.table_name), Identifier("countries"), Identifier("vacation_id"), Placeholder())
            cur.execute(query, (vacation_id,))
            result = cur.fetchone()
             
        return Vacation(vacation_id=result['vacation_id'], country_id=result['country_id'], country_name=result['country_name'],
                        vacation_info=result['vacation_info'],vacation_start_date=result['vacation_start_date'],
                        vacation_end_date=result['vacation_end_date'],price=result['price'], photo_file_path=result['photo_file_path']) if result else None
   
        
    def update_vacation_value_by_id(self, vacation_id: int, column_to_update: str, new_value: str) -> Vacation | None:
        """
        Updates the value of a specific column for a vacation in the 'vacations' table.
        Args: vacation_id (int), column_to_update (str), new_value (str).
        Returns: Vacation: A Vacation object representing the vacation, or None if not found.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("UPDATE {} SET {} = {} WHERE {} = {} RETURNING *").format(
                Identifier(self.table_name), Identifier(column_to_update), Placeholder(), Identifier("vacation_id"),Placeholder())
            cur.execute(query, (new_value, vacation_id))
            self.db_conn.commit()
            result = cur.fetchone()
            
        return Vacation(vacation_id=result['vacation_id'], country_id=result['country_id'], vacation_info=result['vacation_info'],
                        vacation_start_date=result['vacation_start_date'],vacation_end_date=result['vacation_end_date'],price=result['price'],
                        photo_file_path=result['photo_file_path']) if result else None
        
        
    def delete_vacation_by_id(self, vacation_id: int) -> Vacation | None:
        """
        Deletes a vacation from the 'vacations' table by vacation_id.
        Args: vacation_id (int)
        Returns: Vacation: A Vacation object representing the vacation, or None if not found.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("DELETE FROM {} WHERE {} = {} RETURNING *").format(Identifier(self.table_name), Identifier("vacation_id"), Placeholder())
            cur.execute(query, (vacation_id,))
            self.db_conn.commit()
            result = cur.fetchone()

        return Vacation(vacation_id=result['vacation_id'], country_id=result['country_id'], vacation_info=result['vacation_info'],
                        vacation_start_date=result['vacation_start_date'], vacation_end_date=result['vacation_end_date'],
                        price=result['price'], photo_file_path=result['photo_file_path']) if result else None
        
        
    def delete_all_vacations(self) -> None:
        """
        Deletes all vacations from the 'vacations' table.
        Returns: List of Vacations: Vacation objects representing the vacation.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("DELETE FROM {};").format(Identifier(self.table_name))
            cur.execute(query)
            self.db_conn.commit()

# 
