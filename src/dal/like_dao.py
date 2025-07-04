# built-in packages
from typing import List

# internal packages
from src.dal.database import prod_db_conn, dev_db_conn
from src.models.like_dto import Like

# external packages 
from psycopg.sql import SQL, Identifier, Placeholder
import psycopg.rows as pgrows


class LikeDAO:
    def __init__(self, env='prod'):
        self.table_name = "likes"
        self.db_conn = prod_db_conn if env == 'prod' else dev_db_conn


    def get_all_likes(self) -> List[Like]:
        """
        Retrieves all likes from the 'likes' table.
        Returns: List[Like]: A list of Like objects.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {};").format(Identifier(self.table_name))
            cur.execute(query)
            result = cur.fetchall()
            
        return [Like(like_id=row["like_id"], user_id=row["user_id"], vacation_id=row["vacation_id"]) for row in result]
    
    
    def get_liked_vacation_ids_by_user(self, user_id: int) -> List[int]:
        """
        Retrieves a list of vacation_ids that the given user has liked.
        """
        with self.db_conn.cursor() as cur:
            query = SQL("SELECT vacation_id FROM {} WHERE user_id = %s;").format(Identifier(self.table_name))
            cur.execute(query, (user_id,))
            rows = cur.fetchall()
        return [row[0] for row in rows]


    def add_like(self, user_id: int, vacation_id: int) -> Like:
        """
        Adds a new like to the 'likes' table.
        Args: user_id (int), vacation_id (int)
        Returns: Like: The inserted like as a Like object.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(
                Identifier(self.table_name),  
                SQL(", ").join(map(Identifier, ["user_id", "vacation_id"])),
                SQL(", ").join(Placeholder() for _ in range(2)))
            cur.execute(query, (user_id, vacation_id)) 
            self.db_conn.commit()
            result = cur.fetchone()
            
        return Like(like_id=result["like_id"], user_id=result["user_id"], vacation_id=result["vacation_id"])
        
        
    def get_like_by_id(self, like_id: int) -> Like | None:
        """
        Retrieves a like from the 'likes' table by like_id.
        Args: like_id (int).
        Returns: Like: The like as a Like object, or None if not found.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {}").format(Identifier(self.table_name), Identifier("like_id"), Placeholder())
            cur.execute(query, (like_id,))
            result = cur.fetchone()
            
        return Like(like_id=result["like_id"], user_id=result["user_id"], vacation_id=result["vacation_id"]) if result else None
        
        
    def get_like_by_user_and_vacation(self, user_id: int, vacation_id: int) -> Like | None:
        """
        Retrieves a like from the 'likes' table by user_id and vacation_id.
        Args: user_id (int), vacation_id (int).
        Returns: Like: The like as a Like object, or None if not found.
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("SELECT * FROM {} WHERE {} = {} AND {} = {}").format(Identifier(self.table_name), Identifier("user_id"), Placeholder(),
                                                                             Identifier("vacation_id"), Placeholder())
            cur.execute(query, (user_id, vacation_id))
            result = cur.fetchone()
            
        return Like(like_id=result["like_id"], user_id=result["user_id"], vacation_id=result["vacation_id"]) if result else None
    
        
    def update_like_value_by_id(self, like_id: int, column_to_update: str, new_value: int) -> Like | None:
        """
        Updates the value of a specific column for a like in the 'likes' table.
        Args: likes_id (int), column_to_update (str), new_value (str).
         Returns: Like: The updated like as a Like object, or None if not found
        """
        with self.db_conn.cursor() as cur:
            query = SQL("UPDATE {} SET {} = {} WHERE {} = {} RETURNING *").format(
                Identifier(self.table_name), Identifier(column_to_update), Placeholder(), Identifier("like_id"),Placeholder())
            cur.execute(query, (new_value, like_id))
            self.db_conn.commit()
            result = cur.fetchone()
        
        return Like(like_id=result["like_id"], user_id=result["user_id"], vacation_id=result["vacation_id"]) if result else None
        
        
    def delete_like(self, user_id: int, vacation_id: int) -> Like | None:
        """
        Deletes a like from the 'likes' table by like_id.
        Args: like_id (int)
        Returns: Like: The deleted like as a Like object, or None if not found
        """
        with self.db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = SQL("DELETE FROM {} WHERE {} = {} AND {} = {} RETURNING *").format(Identifier(self.table_name), Identifier("user_id"), Placeholder(),
                                                                                 Identifier("vacation_id"), Placeholder())
            cur.execute(query, (user_id, vacation_id))
            self.db_conn.commit()
            result = cur.fetchone()
            
        return Like(like_id=result["like_id"], user_id=result["user_id"], vacation_id=result["vacation_id"]) if result else None

# 
