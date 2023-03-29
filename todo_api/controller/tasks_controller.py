from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from todo_api.services.tasks_services import (
    get_all_tasks,
    get_serialized_task,
    delete_task,
    create_task,
    update_task,
)

tasks = Blueprint('tasks', __name__)


@tasks.route('/todo_api/v1.0/tasks', methods=['GET'])
@jwt_required()
def get_user_tasks():
    user_id = get_jwt_identity()

    tasks_list = get_all_tasks(user_id=user_id)
    return jsonify({'tasks': tasks_list}), 200


@tasks.route('todo_api/v1.0/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task_by_id(task_id: int):
    user_id = get_jwt_identity()

    serialized_task = get_serialized_task(task_id=task_id, user_id=user_id)
    return jsonify(serialized_task), 200


@tasks.route('todo_api/v1.0/tasks', methods=['POST'])
@jwt_required()
def create_new_task():
    user_id = get_jwt_identity()

    serialized_task = create_task(
        title=request.json.get('title').strip(),
        text=request.json.get('text').strip(),
        completion_date=request.json.get('completion_date').strip(),
        user_id=user_id
    )
    return jsonify(serialized_task), 201


@tasks.route('todo_api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task_state(task_id: int):
    user_id = get_jwt_identity()

    serialized_task = update_task(
        task_id=task_id,
        user_id=user_id,
        done=request.json.get('done').strip()
    )
    return jsonify(serialized_task), 200


@tasks.route('todo_api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_user_task(task_id: int):
    user_id = get_jwt_identity()

    delete_task(task_id=task_id, user_id=user_id)
    return {"delete_flag": 0}, 200
