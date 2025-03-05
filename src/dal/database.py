# internal packages
from src.config import conn_info

# external packages
import psycopg as pg

db_conn = pg.connect(conn_info)



