# built-in packages
from typing import List

# internal packages
from src.dal.database import db_conn
from src.models.user import User

# external packages 
from psycopg.sql import SQL, Identifier, Placeholder
import psycopg.rows as pgrows


class UserDAO:
    def __init__(self):
        self.table_name = "users"


    def get_all_users(self) -> List[User]:
        """
        Retrieves all users from the 'users' table.
        Returns: List[User]: A list of User objects.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {};").format(Identifier(self.table_name))
            cur.execute(query)
            result = cur.fetchall()
            
        return [User(user_id=row['user_id'], first_name=row['first_name'], last_name=row['last_name'],
                     email=row['email'], password=row['password'], role_id=row['role_id']) for row in result]


    def add_user(self, first_name: str, last_name: str, email: str, password: str) -> User:
        """
        Add a new user to the 'users' table with the provided details.
        Returns: User: A User object representing the inserted user, including all columns and their values.
        """
        role_id = 1
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(
                Identifier(self.table_name),  
                SQL(", ").join(map(Identifier, ["first_name", "last_name", "email", "password", "role_id"])),
                SQL(", ").join(Placeholder() for _ in range(5)))
            cur.execute(query, (first_name, last_name, email, password, role_id)) 
            db_conn.commit()
            result = cur.fetchone()
            
        return User(user_id=result['user_id'], first_name=result['first_name'], last_name=result['last_name'],
                    email=result['email'], password=result['password'], role_id=result['role_id'])
        
        
    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieves a user from the 'users' table by user_id.
        Args: user_id (int).
        Returns: User: A User object representing the user with the specified user_id, or None if no user is found.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("user_id"), Placeholder())
            cur.execute(query, (user_id,))
            result = cur.fetchall()
            
        if result:
            return User(user_id=result[0]['user_id'], first_name=result[0]['first_name'], last_name=result[0]['last_name'],
                        email=result[0]['email'], password=result[0]['password'], role_id=result[0]['role_id'])
        else:
            return None
        
        
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
        Args: user_id (int).
        Returns: str: A message indicating whether the deletion was successful.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("DELETE FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("user_id"), Placeholder())
            cur.execute(query, (user_id,))
            db_conn.commit()

            return f"Deleted user with user_id {user_id}." if cur.rowcount == 1 else f"Deletion user with user_id {user_id} failed."
        
    
    def get_user_by_email_and_password(self, email: str, password: str) -> User | None:
        """
        Retrieves a user from the 'users' table by email and password.
        Args: email (str), password (str).
        Returns: User: A User object representing the user with the specified email and password, or None if no user is found.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {} AND {} = {}").format(
                Identifier(self.table_name), Identifier("email"), Placeholder(), Identifier("password"), Placeholder())
            cur.execute(query, (email, password))
            result = cur.fetchone()
            
        if result:
            return User(user_id=result['user_id'], first_name=result['first_name'], last_name=result['last_name'],
                        email=result['email'], password=result['password'], role_id=result['role_id'])
        else:
            return None
    
    
    def email_exists(self, email: str) -> bool:
        """
        Checks if an email exists in the database.
        Args: email (str).
        Returns: bool: True if the email exists, False otherwise.
        """
        with db_conn.cursor() as cur:
            query = SQL("SELECT EXISTS (SELECT 1 FROM {} WHERE {} = {})").format(
                Identifier(self.table_name), Identifier("email"), Placeholder()
            )
            cur.execute(query, (email,))
            result = cur.fetchone()

        return result[0]

# 
