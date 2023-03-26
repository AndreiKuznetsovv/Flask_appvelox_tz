from flask import request, Blueprint

import todo_api.errors as error
from todo_api.models import (
    User,
    db_add_func,
)

users = Blueprint('users', __name__)


@users.route('/todo_api/v1.0/sign_up', methods=['POST'])
def registration():
    username = request.json.get('username').strip()
    password = request.json.get('password').strip()

    if not username or not password:
        return error.INVALID_INPUT_422
    elif User.query.filter_by(username=username).first():
        return error.ALREADY_EXIST

    new_user = User(username=username, password=User.hash_password(password=password))
    if not db_add_func(new_user):
        return error.SERVER_ERROR_500
    else:
        token = new_user.get_token()
        return {"access_token": token}


@users.route('/todo_api/v1.0/sign_in', methods=['POST'])
def authentication():
    username = request.json.get('username').strip()
    password = request.json.get('password').strip()

    user = User.authenticate(username=username, password=password)
    if not user:
        return error.UNAUTHORIZED

    token = user.get_token()
    return {"access_token": token}
