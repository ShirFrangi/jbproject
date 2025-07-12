# built-in packages
import os

# internal packages
from src.api import auth_routes, errors_routes, vacation_routes
from src import config

# external packages
from flask import Flask
from flask_wtf import CSRFProtect

def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'ui', 'templates'),
        static_folder=os.path.join(base_dir, 'ui', 'static')
    )

    app.secret_key = os.getenv("SECRET_KEY", "some_secret_key")
    app.config.from_object(config)
    
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(vacation_routes.bp)
    app.register_blueprint(errors_routes.bp)

    return app

#
