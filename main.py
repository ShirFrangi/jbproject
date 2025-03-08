# internal packages
from tests.runner import test_all
from src.dal.database import create_database_if_not_exists
from src.config import db_name, db_conn_info, test_db_name, test_db_conn_info


if __name__ == "__main__":
    create_database_if_not_exists(db_name=db_name, db_conn_info=db_conn_info)
    create_database_if_not_exists(db_name=test_db_name, db_conn_info=test_db_conn_info)
    test_all()

# 
