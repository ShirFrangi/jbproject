# built-in packages
from typing import List

# internal packages
from src.dal.database import db_conn

# external packages 
from psycopg.sql import SQL, Identifier, Placeholder
import psycopg.rows as pgrows


class LikeDAO:
    def __init__(self):
        self.table_name = "likes"


    def get_all_likes(self) -> List[dict]:
        """
        Retrieves all likes from the 'likes' table.
        Returns: List[dict]: A list of dictionaries representing the likes in the table. Each dictionary contains column-value pairs for a like.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {};").format(Identifier(self.table_name))
            cur.execute(query)
            result = cur.fetchall()
            
        return result


    def add_like(self, user_id: int, vacation_id: int) -> dict:
        """
        Add a new like to the 'likes' table with the provided details.
        Args: user_id (int), vacation_id (int)
        Returns: dict: A dictionary representing the inserted like, including all columns and their values.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(
                Identifier(self.table_name),  
                SQL(", ").join(map(Identifier, ["user_id", "vacation_id"])),
                SQL(", ").join(Placeholder() for _ in range(2)))
            cur.execute(query, (user_id, vacation_id)) 
            db_conn.commit()
            result = cur.fetchone()
            
        return result
        
        
    def get_like_by_id(self, like_id: int) -> dict | None:
        """
        Retrieves a like from the 'likes' table by like_id.
        Args: user_id (int)
        Returns: dict: A dictionary representing the like with the specified like_id, or None if no like is found.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("like_id"), Placeholder())
            cur.execute(query, (like_id,))
            result = cur.fetchall()
            
        return result
        
        
    def update_like_value_by_id(self, like_id: int, column_to_update: str, new_value: str) -> str:
        """
        Updates the value of a specific column for a like in the 'likes' table.
        Args: likes_id (int), column_to_update (str), new_value (str).
        Returns: str: A message indicating whether the update was successful.
        """
        with db_conn.cursor() as cur:
            query = SQL("UPDATE {} SET {} = {} WHERE {} = {}").format(
                Identifier(self.table_name), Identifier(column_to_update), Placeholder(), Identifier("like_id"),Placeholder())
            cur.execute(query, (new_value, like_id))
            db_conn.commit()
            
            return f"Updated like with like_id {like_id}." if cur.rowcount == 1 else f"Update like with like_id {like_id} failed."
        
        
    def delete_like(self, user_id: int, vacation_id: id) -> str:
        """
        Deletes a like from the 'likes' table by like_id.
        Args: like_id (int)
        Returns: str: A message indicating whether the deletion was successful.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("DELETE FROM {} WHERE {} = {} AND WHERE {} = {}").format(Identifier(self.table_name), Identifier("user_id"), Placeholder(),
                                                                                 Identifier("vacation_id"), Placeholder())
            cur.execute(query, (user_id, vacation_id))
            db_conn.commit()

            return f"Deleted like for user with user_id {user_id}." if cur.rowcount == 1 else f"Deletion like for user with user_id {user_id} failed."

# 
