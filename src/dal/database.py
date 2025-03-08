# built-in packages
import os

# internal packages
from src.config import db_conn_info, test_db_conn_info

# external packages
import psycopg as pg
from psycopg.rows import dict_row

try:
    prod_db_conn = pg.connect(db_conn_info)
    test_db_conn = pg.connect(test_db_conn_info)

except Exception as e:
    print(f"Error connecting to DB: {e}")


def initialize_database(env='dev') -> str:
    """
    Initializes the database by dropping existing tables and recreating them 
    using SQL commands from the 'init_db.sql' file.
    """
    data_base = test_db_conn if env == 'dev' else prod_db_conn
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file_path = current_dir.replace('dal', 'init_db.sql')
    try:
        with open(sql_file_path, 'r') as sql_file:
            sql_commands = sql_file.read()
        with data_base.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "DROP TABLE IF EXISTS users, countries, likes, roles, vacations;")
            cur.execute(sql_commands)
            data_base.commit()

    except Exception as e:
        print(f"Error initializing database: {e}")
        data_base.rollback()


def create_database_if_not_exists(db_conn_info, db_name):
    """
    This function checks if the database exists and if not creates it.
    """
    try:
        with pg.connect(db_conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
                exists = cur.fetchone()

                if not exists:
                    print(f"Database '{db_name}' does not exist. Creating...")
                    cur.execute(f"CREATE DATABASE {db_name}")
                    print(f"Database '{db_name}' created successfully.")

    except Exception as e:
        print(f"Error while creating database: {e}")


#
