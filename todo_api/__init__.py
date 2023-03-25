from flask import Flask

def create_app():
    # create an app
    app = Flask(__name__)

    # import development config class
    from todo_api.config import DevelopmentConfig
    # load config from config.py file
    app.config.from_object(DevelopmentConfig)

    return app