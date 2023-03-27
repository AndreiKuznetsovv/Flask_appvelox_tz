from flask import request, Blueprint, jsonify
from todo_api.models import User, Task, db_add_func, db_commit_func, db_delete_func
from flask_jwt_extended import jwt_required, get_jwt_identity
import todo_api.errors as error
from datetime import date

tasks = Blueprint('tasks', __name__)


@tasks.route('/todo_api/v1.0/tasks', methods=['GET'])
@jwt_required()
def get_user_tasks():
    user_id = get_jwt_identity()

    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.completion_date.asc()).all()
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'title': task.title,
            'text': task.text,
            'completion_date': str(task.completion_date),
            'done': task.done,
            'user_id': task.author.id,
        })
    return jsonify({'tasks': tasks_list}), 200


@tasks.route('todo_api/v1.0/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task_by_id(task_id: int):
    user_id = get_jwt_identity()

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return error.DOES_NOT_EXIST

    return jsonify({'title': task.title,
                    'text': task.text,
                    'completion_date': str(task.completion_date),
                   'done': task.done}), 200


@tasks.route('todo_api/v1.0/tasks', methods=['POST'])
@jwt_required()
def create_new_task():
    user_id = get_jwt_identity()

    title = request.json.get('title').strip()
    text = request.json.get('text').strip()
    completion_date = request.json.get('completion_date').strip()

    if not title or not text or not completion_date:
        return error.INVALID_INPUT_422

    completion_date_list = completion_date.split('-')
    year, month, day = map(int, completion_date_list)

    new_task = Task(title=title, text=text, completion_date=date(year, month, day), user_id=user_id)
    if not db_add_func(new_task):
        return error.SERVER_ERROR_500
    else:
        return jsonify({'title': new_task.title,
                        'text': new_task.text,
                        'completion_date': str(new_task.completion_date),
                        'done': new_task.done}), 201


@tasks.route('todo_api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task_state(task_id: int):
    user_id = get_jwt_identity()

    done = request.json.get('done').strip()
    if not done:
        return error.INVALID_INPUT_422

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return error.DOES_NOT_EXIST

    task.done = bool(done)

    if not db_commit_func():
        return error.SERVER_ERROR_500
    else:
        return jsonify({'title': task.title,
                        'text': task.text,
                        'completion_date': str(task.completion_date),
                        'done': task.done}), 200


@tasks.route('todo_api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id: int):
    user_id = get_jwt_identity()

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return error.DOES_NOT_EXIST

    if not db_delete_func(task):
        return error.SERVER_ERROR_500
    else:
        return {"delete_flag": 0}, 200

