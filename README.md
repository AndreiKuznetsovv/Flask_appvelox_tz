# Test task for appvelox

* [General info](#general-info)
* [Functionality](#functionality)
* [Technologies](#technologies)

## General info

RESTful API to do list

Methods HTTP URI for Tasks 
* GET http://[hostname]/todo_api/v1.0/tasks - Get list of all user tasks
* GET http://[hostname]/todo_api/v1.0/tasks/[task_id] - Get user task by id
* POST http://[hostname]/todo_api/v1.0/tasks - Make new task 
* PUT http://[hostname]/todo_api/v1.0/tasks/[task_id] - Update state of task
* DELETE http://[hostname]/todo_api/v1.0/tasks/[task_id] - Delete task

Methods HTTP URI for Users
* POST http://[hostname]/todo/api/v1.0/sign_up - Registrate new user
* POST http://[hostname]/todo/api/v1.0/sign_in - Authenticate user


## Functionality

* get list off tasks
* make a new task
* get a specific task by id
* mark task as completed 
* delete task

## Technologies
* Flask
* Postgres
* ...