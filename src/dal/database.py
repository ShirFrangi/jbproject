# built-in packages
import os

# internal packages
from src.config import conn_info

# external packages
import psycopg as pg
import psycopg.rows as pgrows


db_conn = pg.connect(conn_info)


def initialize_database() -> str:
    """
    Initializes the database by dropping existing tables and recreating them 
    using SQL commands from the 'init_db.sql' file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file_path = current_dir.replace('dal', 'init_db.sql')
    try:
        with open(sql_file_path, 'r') as sql_file:
            sql_commands = sql_file.read()
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute("DROP TABLE IF EXISTS users, countries, likes, roles, vacations;")
            cur.execute(sql_commands)
            db_conn.commit()
            print("Database tables dropped and recreated successfully.")
    
    except Exception as e:
        print(f"Error initializing database: {e}")
        db_conn.rollback()

# 
        