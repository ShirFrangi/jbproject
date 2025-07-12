# internal packages
from tests.runner import test_all
from src.api import create_app
from src.dal.database import initialize_database


if __name__ == "__main__":
    # -- Running Tests --
    test_all()
    initialize_database()
    
    # -- Running Application --
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)

#
