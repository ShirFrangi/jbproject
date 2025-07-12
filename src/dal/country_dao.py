# built-in packages
from typing import List

# internal packages
from src.dal.database import prod_db_conn, dev_db_conn
from src.models.country_dto import Country

# external packages 
from psycopg.sql import SQL, Identifier, Placeholder
import psycopg.rows as pgrows


class CountryDAO:
    def __init__(self, env: str ='prod'):
        self.table_name = "countries"
        self.db_conn = prod_db_conn if env == 'prod' else dev_db_conn


    def get_all_countries(self) -> List[Country]:
        """
        Retrieves all countries from the 'countries' table.
        Returns: List[Country]: A list of Country objects representing the countries in the table.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {};").format(Identifier(self.table_name))
            cur.execute(query)
            result = cur.fetchall()
        
        countries = [Country(country_id=row["country_id"], country_name=row["country_name"]) for row in result]
        
        return countries


    def add_country(self, country_name: str) -> Country:
        """
        Add a new country to the 'countries' table with the provided details.
        Args: country_name (str).
        Returns: dict: A dictionary representing the inserted country.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(
                Identifier(self.table_name), Identifier("country_name"), Placeholder())
            cur.execute(query, (country_name,)) 
            self.db_conn.commit()
            result = cur.fetchone()
            
        return Country(country_id=result["country_id"], country_name=result["country_name"])

        
    def get_country_by_id(self, country_id: int) -> Country | None:
        """
        Retrieves a country from the 'countries' table by country_id.
        Args: country_id (int)
        Returns: Country: A Country object representing the country, or None if not found.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("country_id"), Placeholder())
            cur.execute(query, (country_id,))
            result = cur.fetchone()
            
        return Country(country_id=result["country_id"], country_name=result["country_name"]) if result else None
        
        
    def update_country_value_by_id(self, country_id: int, column_to_update: str, new_value: str) -> Country| None:
        """
        Updates the value of a specific column for a country in the 'countries' table.
        Args: country_id (int), column_to_update (str), new_value (str).
        Returns: Country: A Country object representing the country, or None if not found.
        """
        with self.db_conn.cursor() as cur:
            query = SQL("UPDATE {} SET {} = {} WHERE {} = {} RETURNING *").format(
                Identifier(self.table_name), Identifier(column_to_update), Placeholder(), Identifier("country_id"),Placeholder())
            cur.execute(query, (new_value, country_id))
            self.db_conn.commit()
            result = cur.fetchone()
            
        return Country(country_id=result["country_id"], country_name=result["country_name"]) if result else None
        
        
    def delete_country_by_id(self, country_id: int) -> Country | None:
        """
        Deletes a country from the 'countries' table by country_id.
        Args: country_id (int)
        Returns: Country: A Country object representing the country, or None if not found.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("DELETE FROM {} WHERE {} = {} RETURNING *").format(Identifier(self.table_name), Identifier("country_id"), Placeholder())
            cur.execute(query, (country_id,))
            self.db_conn.commit()
            result = cur.fetchone()
            
        return Country(country_id=result["country_id"], country_name=result["country_name"]) if result else None

# 
