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
        db, migrate,
        jwt
    )

    db.init_app(app)  # initialize the database
    migrate.init_app(app, db)  # initialize the flask migrate (Flask wrapper for Alembic)
    jwt.init_app(app)

    from todo_api.users.views import users
    from todo_api.tasks.views import tasks

    app.register_blueprint(users, url_prefix="/")
    app.register_blueprint(tasks, url_prefix="/")

    return app