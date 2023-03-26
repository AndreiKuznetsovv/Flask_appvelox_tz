from flask import request, Blueprint
from todo_api.models import User, Task
from flask_jwt_extended import jwt_required

tasks = Blueprint('tasks', __name__)


@tasks.route('/todo_api/v1.0/tasks', methods=['GET'])
@jwt_required
def get_all_tasks():
    return {'payload': 'all tasks'}