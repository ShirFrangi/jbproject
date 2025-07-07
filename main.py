# internal packages
from tests.runner import test_all
from src.api.app import app
from src.dal.database import initialize_database


if __name__ == "__main__":
    test_all()
    initialize_database('prod')
    app.run(host='0.0.0.0', port=5001, debug=True)

#
