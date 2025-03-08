# internal packages
from tests.runner import test_all
from src.dal.database import create_database_if_not_exists
from src.config import prod_db_name, prod_db_conn_info, dev_db_name, dev_db_conn_info


if __name__ == "__main__":
    create_database_if_not_exists(db_name=prod_db_name, db_conn_info=prod_db_conn_info)
    create_database_if_not_exists(db_name=dev_db_name, db_conn_info=dev_db_conn_info)
    # test_all()

#
