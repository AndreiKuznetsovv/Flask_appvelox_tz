from datetime import date

from flask import abort

from todo_api.models.models import Task
from .db_services import (
    db_add_func,
    db_commit_func,
    db_delete_func,
)


def serialize_task(task: Task) -> dict:
    serialized_task = {'title': task.title,
                       'text': task.text,
                       'completion_date': str(task.completion_date),
                       'done': task.done}
    return serialized_task


def get_all_tasks(user_id: int) -> list:
    tasks = Task.query.filter_by(user_id=user_id) \
        .order_by(Task.completion_date.asc()).all()
    serialized_tasks = []
    for task in tasks:
        serialized_tasks.append({
            'title': task.title,
            'text': task.text,
            'completion_date': str(task.completion_date),
            'done': task.done,
            'user_id': task.author.id,
        })
        return serialized_tasks


def get_one_task(task_id: int, user_id: int) -> Task:
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        abort(404)
    return task


def get_serialized_task(task_id: int, user_id: int) -> dict:
    task = get_one_task(task_id=task_id, user_id=user_id)

    serialized_task = serialize_task(task)
    return serialized_task


def create_task(
        title: str,
        text: str,
        completion_date: str,
        user_id: int
) -> dict:
    if not title or not text or not completion_date:
        abort(422)

    year, month, day = map(int, completion_date.split('-'))

    new_task = Task(title=title, text=text,
                    completion_date=date(year, month, day), user_id=user_id)

    if not db_add_func(new_task):
        abort(500)

    serialized_task = serialize_task(new_task)
    return serialized_task


def update_task(task_id: int, user_id: int, done: str) -> dict:
    if not done:
        abort(422)

    task = get_one_task(task_id=task_id, user_id=user_id)
    task.done = bool(done)

    if not db_commit_func():
        abort(500)

    serialized_task = serialize_task(task)
    return serialized_task


def delete_task(task_id: int, user_id: int) -> None:
    task = get_one_task(task_id=task_id, user_id=user_id)

    if not db_delete_func(task):
        abort(500)
