from sqlalchemy.exc import SQLAlchemyError

from todo_api.models.models import db


def db_add_func(data):
    try:
        db.session.add(data)
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def db_delete_func(data):
    try:
        db.session.delete(data)
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def db_commit_func():
    try:
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False
