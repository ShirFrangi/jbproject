# built-in packages
from typing import List, Optional

# internal packages
from src.dal.database import db_conn

# external packages 
from psycopg.sql import SQL, Identifier, Placeholder
import psycopg.rows as pgrows


class CountryDAO:
    def __init__(self):
        self.table_name = "countries"


    def get_all_countries(self) -> List[dict]:
        """
        Retrieves all countries from the 'countries' table.
        Returns: List[dict]: A list of dictionaries representing the countries in the table. Each dictionary contains column-value pairs for a country.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {};").format(Identifier(self.table_name))
            cur.execute(query)
            result = cur.fetchall()
            
        return result


    def add_country(self, country_name: str) -> dict:
        """
        Add a new country to the 'countries' table with the provided details.
        Args: country_name (str).
        Returns: dict: A dictionary representing the inserted country.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(
                Identifier(self.table_name), Identifier("country_name"), Placeholder())
            cur.execute(query, (country_name,)) 
            db_conn.commit()
            result = cur.fetchone()
            
        return result

        
    def get_country_by_id(self, country_id: int) -> Optional[dict]:
        """
        Retrieves a country from the 'countries' table by country_id.
        Args: country_id (int)
        Returns: dict: A dictionary representing the country with the specified country_id, or None if no country is found.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("country_id"), Placeholder())
            cur.execute(query, (country_id,))
            result = cur.fetchall()
            
        return result
        
        
    def update_country_value_by_id(self, country_id: int, column_to_update: str, new_value: str) -> str:
        """
        Updates the value of a specific column for a country in the 'countries' table.
        Args: country_id (int), column_to_update (str), new_value (str).
        Returns: str: A message indicating whether the update was successful.
        """
        with db_conn.cursor() as cur:
            query = SQL("UPDATE {} SET {} = {} WHERE {} = {}").format(
                Identifier(self.table_name), Identifier(column_to_update), Placeholder(), Identifier("country_id"),Placeholder())
            cur.execute(query, (new_value, country_id))
            db_conn.commit() 
            
            return f"Updated country with country_id {country_id}." if cur.rowcount == 1 else f"Update country with country_id {country_id} failed."
        
        
    def delete_country_by_id(self, country_id: int) -> str:
        """
        Deletes a country from the 'countries' table by country_id.
        Args: country_id (int)
        Returns: str: A message indicating whether the deletion was successful.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("DELETE FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("country_id"), Placeholder())
            cur.execute(query, (country_id,))
            db_conn.commit()
            affected_rows = cur.rowcount
            
            return f"Deleted country with country_id {country_id}." if cur.rowcount == 1 else f"Deletion country with country_id {country_id} failed."

# 
