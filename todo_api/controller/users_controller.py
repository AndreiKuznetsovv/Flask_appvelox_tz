from flask import request, Blueprint

from todo_api.services.users_services import registrate, authenticate

users = Blueprint('users', __name__)


@users.route('/todo_api/v1.0/sign_up', methods=['POST'])
def registration():
    token = registrate(
        username=request.json.get('username').strip(),
        password=request.json.get('password').strip()
    )
    return {"access_token": token}, 201


@users.route('/todo_api/v1.0/sign_in', methods=['POST'])
def authentication():
    token = authenticate(
        username=request.json.get('username').strip(),
        password=request.json.get('password').strip()
    )
    return {"access_token": token}, 200
