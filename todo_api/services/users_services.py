from datetime import timedelta

from flask import abort
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from todo_api.models.models import User
from .db_services import db_add_func


def hash_password(password: str) -> str:
    return generate_password_hash(password, method='sha256')


def verify_password(hashed_password: str, password: str) -> bool:
    return check_password_hash(pwhash=hashed_password, password=password)


def get_user(username: str) -> User:
    user = User.query.filter_by(username=username).first()
    return user


def authenticate(username: str, password: str) -> str:
    user = get_user(username=username)
    if not user or not \
            verify_password(hashed_password=user.password, password=password):
        abort(401)
    token = get_token(user=user)
    return token


def get_token(user: User, expire_time=24) -> str:
    expire_delta = timedelta(expire_time)
    token = create_access_token(
        identity=user.id,
        expires_delta=expire_delta
    )
    return token


def registrate(username: str, password: str):
    if not username or not password:
        abort(422)
    elif get_user(username=username):
        abort(409)

    new_user = User(username=username, password=hash_password(password=password))
    if not db_add_func(new_user):
        abort(500)
    else:
        token = get_token(user=new_user)
        return token
