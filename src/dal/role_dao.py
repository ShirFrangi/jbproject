# built-in packages
from typing import List

# internal packages
from src.dal.database import prod_db_conn, dev_db_conn
from src.models.role_dto import Role

# external packages 
from psycopg.sql import SQL, Identifier, Placeholder
import psycopg.rows as pgrows


class RoleDAO:
    def __init__(self, env: str ='prod'):
        self.table_name = "roles"
        self.db_conn = prod_db_conn if env == 'prod' else dev_db_conn


    def get_all_roles(self) -> List[Role]:
        """
        Retrieves all roles from the 'roles' table.
        Returns: List[Role]: A list of Role enum objects.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {};").format(Identifier(self.table_name))
            cur.execute(query)
            result = cur.fetchall()
            
        return [Role(row['role_name']) for row in result]


    def add_role(self, role_name: str) -> Role:
        """
        Add a new role to the 'roles' table with the provided details.
        Args: role_name (str).
        Returns: Role: A Role enum object representing the inserted role.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(Identifier(self.table_name), Identifier("role_name"), Placeholder())
            cur.execute(query, (role_name,))
            result = cur.fetchone()
            
        return Role(result['role_name'])
        
        
    def get_role_by_id(self, role_id: int) -> Role | None:
        """
        Retrieves a role from the 'roles' table by role_id.
        Args: role_id (int).
        Returns: Role: A Role enum object, or None if no role is found.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("role_id"), Placeholder())
            cur.execute(query, (role_id,))
            result = cur.fetchone()
            
        return Role(result['role_name']) if result else None
        
        
    def update_role_value_by_id(self, role_id: int, column_to_update: str, new_value: str) -> Role | None:
        """
        Updates the value of a specific column for a role in the 'roles' table.
        Args: roles_id (int), column_to_update (str), new_value (str).
        Returns: Role: A Role enum object, or None if no role is found.
        """
        with self.db_conn.cursor() as cur:
            query = SQL("UPDATE {} SET {} = {} WHERE {} = {} RETURNING *").format(
                Identifier(self.table_name), Identifier(column_to_update), Placeholder(), Identifier("role_id"),Placeholder())
            cur.execute(query, (new_value, role_id))
            self.db_conn.commit()
            result = cur.fetchone()
            
        return Role(result['role_name']) if result else None
        
        
    def delete_role_by_id(self, role_id: int) -> Role | None:
        """
        Deletes a role from the 'roles' table by role_id.
        Args: role_id (int)
        Returns: Role: A Role enum object, or None if no role is found.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("DELETE FROM {} WHERE {} = {} RETURNING *").format(Identifier(self.table_name), Identifier("role_id"), Placeholder())
            cur.execute(query, (role_id,))
            self.db_conn.commit()
            result = cur.fetchone()

        return Role(result['role_name']) if result else None

# 
