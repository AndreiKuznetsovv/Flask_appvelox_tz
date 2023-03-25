from flask import Flask

def create_app():
    # create an app
    app = Flask(__name__)

    # import development config class
    from todo_api.config import DevelopmentConfig
    # load config from config.py file
    app.config.from_object(DevelopmentConfig)

    from .models import (
        User, Task,
        db, migrate
    )

    db.init_app(app) # initialize the database
    migrate.init_app(app, db) # initialize the flask migrate (Flask wrapper for Alembic)

    return app