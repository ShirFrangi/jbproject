# built-in packages
from typing import List

# internal packages
from src.dal.database import prod_db_conn, dev_db_conn
from src.models.user_dto import User

# external packages 
from psycopg.sql import SQL, Identifier, Placeholder
import psycopg.rows as pgrows


class UserDAO:
    def __init__(self, env: str ='prod'):
        self.table_name = "users"
        self.db_conn = prod_db_conn if env == 'prod' else dev_db_conn


    def get_all_users(self) -> List[User]:
        """
        Retrieves all users from the 'users' table.
        Returns: List[User]: A list of User objects.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {};").format(Identifier(self.table_name))
            cur.execute(query)
            result = cur.fetchall()
            
        return [User(user_id=row['user_id'], first_name=row['first_name'], last_name=row['last_name'],
                     email=row['email'], hashed_password=row['hashed_password'], role_id=row['role_id']) for row in result]


    def add_user(self, first_name: str, last_name: str, email: str, hashed_password: str) -> User:
        """
        Add a new user to the 'users' table with the provided details.
        Returns: User: A User object representing the inserted user, including all columns and their values.
        """
        role_id = 1
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("INSERT INTO {} (first_name, last_name, email, hashed_password, role_id) VALUES (%s, %s, %s, %s, %s) RETURNING *").format(
                Identifier(self.table_name))
            cur.execute(query, (first_name, last_name, email, hashed_password, role_id))
            self.db_conn.commit()
            result = cur.fetchone()
        
        return User(user_id=result['user_id'], first_name=result['first_name'], last_name=result['last_name'],
                    email=result['email'], hashed_password=result['hashed_password'], role_id=result['role_id'])

        
    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieves a user from the 'users' table by user_id.
        Args: user_id (int).
        Returns: User: A User object representing the user with the specified user_id, or None if no user is found.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("user_id"), Placeholder())
            cur.execute(query, (user_id,))
            result = cur.fetchone()
            
        
        return User(user_id=result['user_id'], first_name=result['first_name'], last_name=result['last_name'],
                    email=result['email'], hashed_password=result['hashed_password'], role_id=result['role_id']) if result else None
        
        
    def update_user_value_by_id(self, user_id: int, column_to_update: str, new_value: str) -> User | None:
        """
        Updates the value of a specific column for a user in the 'users' table.
        Args: user_id (int), column_to_update (str), new_value (str).
        Returns: User: A User object representing the user, or None if not found.
        """
        with self.db_conn.cursor() as cur:
            query = SQL("UPDATE {} SET {} = {} WHERE {} = {} RETURNING *").format(
                Identifier(self.table_name), Identifier(column_to_update), Placeholder(), Identifier("user_id"),Placeholder())
            cur.execute(query, (new_value, user_id))
            self.db_conn.commit()
            result = cur.fetchone()
            
        return User(user_id=result['user_id'], first_name=result['first_name'], last_name=result['last_name'],
                email=result['email'], hashed_password=result['hashed_password'], role_id=result['role_id']) if result else None
        
        
    def delete_user_by_id(self, user_id: int) -> User | None:
        """
        Deletes a user from the 'users' table by user_id.
        Args: user_id (int).
        Returns: User: A User object representing the user, or None if not found.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("DELETE FROM {} WHERE {} = {} RETURNING *").format(Identifier(self.table_name), Identifier("user_id"), Placeholder())
            cur.execute(query, (user_id,))
            self.db_conn.commit()
            result = cur.fetchone()

        return User(user_id=result['user_id'], first_name=result['first_name'], last_name=result['last_name'],
               email=result['email'], hashed_password=result['hashed_password'], role_id=result['role_id']) if result else None
        
    
    def get_user_by_email_and_password(self, email: str, hashed_password: str) -> User | None:
        """
        Retrieves a user from the 'users' table by email and hashed_password.
        Args: email (str), hashed_password (str).
        Returns: User: A User object representing the user with the specified email and hashed_password, or None if no user is found.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {} AND {} = {}").format(
                Identifier(self.table_name), Identifier("email"), Placeholder(), Identifier("hashed_password"), Placeholder())
            cur.execute(query, (email, hashed_password))
            result = cur.fetchone()
            
        
        return User(user_id=result['user_id'], first_name=result['first_name'], last_name=result['last_name'],
                    email=result['email'], hashed_password=result['hashed_password'], role_id=result['role_id']) if result else None
        
    
    def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieves a user from the 'users' table by email.
        Args: email (str).
        Returns: User: A User object representing the user with the specified email and hashed_password, or None if no user is found.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {}").format(
                Identifier(self.table_name), Identifier("email"), Placeholder())
            cur.execute(query, (email,))
            result = cur.fetchone()
            
        
        return User(user_id=result['user_id'], first_name=result['first_name'], last_name=result['last_name'],
                    email=result['email'], hashed_password=result['hashed_password'], role_id=result['role_id']) if result else None
    
    
    def email_exists(self, email: str) -> bool:
        """
        Checks if an email exists in the database.
        Args: email (str).
        Returns: bool: True if the email exists, False otherwise.
        """
        with self.db_conn.cursor() as cur:
            query = SQL("SELECT EXISTS (SELECT 1 FROM {} WHERE {} = {})").format(
                Identifier(self.table_name), Identifier("email"), Placeholder()
            )
            cur.execute(query, (email,))
            result = cur.fetchone()

        return result[0]

# 
