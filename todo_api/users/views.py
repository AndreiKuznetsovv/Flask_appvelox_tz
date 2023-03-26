from flask import request, Blueprint

import todo_api.errors as error
from todo_api.models import (
    User,
    db_add_func,
)
from flask_jwt_extended import JWTManager

users = Blueprint('users', __name__)
jwt = JWTManager()

@users.route('/todo_api/v1.0/sign_up', methods=['POST'])
def sign_up():
    username = request.json.get('username').strip() or None
    password = request.json.get('password').strip() or None
    if username is None or password is None:
        return error.INVALID_INPUT_422
    elif User.query.filter_by(username=username).first():
        return error.ALREADY_EXIST

    new_user = User(username=username, password=User.hash_password(password=password))
    if db_add_func(new_user):
        token = new_user.get_token()
        return {"access_token": token}
    else:
        return error.SERVER_ERROR_500


@users.route('/todo_api/v1.0/sign_in', methods=['POST'])
def sign_in():
    username = request.json.get('username').strip()
    password = request.json.get('password').strip()

    user = User.authenticate(username=username, password=password)
    if not user:
        return error.INVALID_INPUT_422

    token = user.get_token()
    return {"access_token": token}