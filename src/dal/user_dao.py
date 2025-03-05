# built-in packages
from typing import List, Optional

# internal packages
from src.dal.database import db_conn

# external packages 
from psycopg.sql import SQL, Identifier, Placeholder
import psycopg.rows as pgrows


class UserDAO:
    def __init__(self):
        self.table_name = "users"


    def get_all_users(self) -> List[dict]:
        """
        Retrieves all users from the 'users' table.
        Returns: List[dict]: A list of dictionaries representing the users in the table. Each dictionary contains column-value pairs for a user.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {};").format(Identifier(self.table_name))
            cur.execute(query)
            result = cur.fetchall()
            
        return result


    def add_user(self, first_name: str, last_name: str, email: str, password: str) -> dict:
        """
        Add a new user to the 'users' table with the provided details.
        Args: first_name (str), last_name (str), email (str), password (str).
        Returns: dict: A dictionary representing the inserted user, including all columns and their values.
        """
        role_id = 1
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(
                Identifier(self.table_name),  
                SQL(", ").join(map(Identifier, ["first_name", "last_name", "email", "password", "role_id"])),
                SQL(", ").join(Placeholder() for _ in range(5)))
            cur.execute(query, (first_name, last_name, email, password, role_id)) 
            db_conn.commit()
            result = cur.fetchone()
            
        return result
        
        
    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """
        Retrieves a user from the 'users' table by user_id.
        Args: user_id (int)
        Returns: dict: A dictionary representing the user with the specified user_id, or None if no user is found.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("user_id"), Placeholder())
            cur.execute(query, (user_id,))
            result = cur.fetchall()
            
        return result
        
        
    def update_user_value_by_id(self, user_id: int, column_to_update: str, new_value: str) -> str:
        """
        Updates the value of a specific column for a user in the 'users' table.
        Args: user_id (int), column_to_update (str), new_value (str).
        Returns: str: A message indicating whether the update was successful.
        """
        with db_conn.cursor() as cur:
            query = SQL("UPDATE {} SET {} = {} WHERE {} = {}").format(
                Identifier(self.table_name), Identifier(column_to_update), Placeholder(), Identifier("user_id"),Placeholder())
            cur.execute(query, (new_value, user_id))
            db_conn.commit()
            
            return f"Updated user with user_id {user_id}." if cur.rowcount == 1 else f"Update user with user_id {user_id} failed."
        
        
    def delete_user_by_id(self, user_id: int) -> str:
        """
        Deletes a user from the 'users' table by user_id.
        Args: user_id (int)
        Returns: str: A message indicating whether the deletion was successful.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("DELETE FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("user_id"), Placeholder())
            cur.execute(query, (user_id,))
            db_conn.commit()

            return f"Deleted user with user_id {user_id}." if cur.rowcount == 1 else f"Deletion user with user_id {user_id} failed."

# 
