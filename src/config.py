# built-in packages
import os

# --- Database connection details - PROD environment ---
prod_db_name = 'jbproject_prod'
prod_db_conn_info = f"postgresql://postgres:postgres@localhost:5432/{prod_db_name}"

# --- Database connection details - DEV environment ---
dev_db_name = 'jbproject_dev'
dev_db_conn_info = f"postgresql://postgres:postgres@localhost:5432/{dev_db_name}"

# --- Application Environment Configuration ('dev'/'prod') ---
test_env = 'dev'
display_env = 'dev'

# --- Default path for saving files - vacation photos ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "ui", "static", "images", "vacation_images")

#
