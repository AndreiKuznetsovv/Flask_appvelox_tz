from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from flask_jwt_extended import create_access_token
from datetime import timedelta

# creation of db object
db = SQLAlchemy()
# creation of migrate object
migrate = Migrate()


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
        db.session.commit(data)
        return True
    except SQLAlchemyError:
        return False


def db_commit_func():
    try:
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # one-to-many relationship for users and tasks
    tasks = db.relationship('Task', backref='author',
                            passive_deletes=True, lazy=True)
    @staticmethod
    def hash_password(password):
        hashed_password = generate_password_hash(password, method='sha256')
        return hashed_password

    def verify_password(self, password):
        return check_password_hash(pwhash=self.password, password=password)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if not user:
            return False
        elif not user.verify_password(password=password):
            return False
        return user

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id,
            expires_delta=expire_delta,
        )
        return token

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    completion_date = db.Column(db.Date(), nullable=False)
    done = db.Column(db.Boolean(), nullable=False)
    # foreign key to table User (tablename users in postgres)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"Task('{self.id}', '{self.title}')"
