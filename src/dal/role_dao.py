# built-in packages
from typing import List, Optional

# internal packages
from src.dal.database import db_conn

# external packages 
from psycopg.sql import SQL, Identifier, Placeholder
import psycopg.rows as pgrows


class RoleDAO:
    def __init__(self):
        self.table_name = "roles"


    def get_all_roles(self) -> List[dict]:
        """
        Retrieves all roles from the 'roles' table.
        Returns: List[dict]: A list of dictionaries representing the roles in the table. Each dictionary contains column-value pairs for a role.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {};").format(Identifier(self.table_name))
            cur.execute(query)
            result = cur.fetchall()
            
        return result


    def add_role(self, role_name: str) -> dict:
        """
        Add a new role to the 'roles' table with the provided details.
        Args: role_name (str).
        Returns: dict: A dictionary representing the inserted role, including all columns and their values.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(Identifier(self.table_name), Identifier("role_name"), Placeholder())
            cur.execute(query, (role_name,))
            result = cur.fetchall()
            
        return result
        
        
    def get_role_by_id(self, role_id: int) -> Optional[dict]:
        """
        Retrieves a role from the 'roles' table by role_id.
        Args: role_id (int).
        Returns: dict: A dictionary representing the role with the specified role_id, or None if no role is found.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("role_id"), Placeholder())
            cur.execute(query, (role_id,))
            result = cur.fetchall()
            
        return result
        
        
    def update_role_value_by_id(self, role_id: int, column_to_update: str, new_value: str) -> str:
        """
        Updates the value of a specific column for a role in the 'roles' table.
        Args: roles_id (int), column_to_update (str), new_value (str).
        Returns: str: A message indicating whether the update was successful.
        """
        with db_conn.cursor() as cur:
            query = SQL("UPDATE {} SET {} = {} WHERE {} = {}").format(
                Identifier(self.table_name), Identifier(column_to_update), Placeholder(), Identifier("role_id"),Placeholder())
            cur.execute(query, (new_value, role_id))
            db_conn.commit()
            
            return f"Updated role with role_id {role_id}." if cur.rowcount == 1 else f"Update role with role_id {role_id} failed."
        
        
    def delete_role_by_id(self, role_id: int) -> str:
        """
        Deletes a role from the 'roles' table by role_id.
        Args: role_id (int)
        Returns: str: A message indicating whether the deletion was successful.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("DELETE FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("role_id"), Placeholder())
            cur.execute(query, (role_id,))
            db_conn.commit()

            return f"Deleted role with role_id {role_id}." if cur.rowcount == 1 else f"Deletion role with role_id {role_id} failed."

# 
