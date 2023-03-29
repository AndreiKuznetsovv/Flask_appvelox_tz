from flask import Blueprint

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def page_not_found(e):
    return ({"message": "Resource could not be found."}, 404)


@errors.app_errorhandler(422)
def invalid_input(e):
    return ({"message": "Invalid input."}, 422)


@errors.app_errorhandler(409)
def already_exists(e):
    return ({"message": "Already exists."}, 409)


@errors.app_errorhandler(500)
def server_error(e):
    return ({"message": "An internal server error occurred."}, 500)


@errors.app_errorhandler(401)
def unauthorized(e):
    return ({"message": "Wrong credentials."}, 401)


@errors.app_errorhandler(405)
def method_not_allowed(e):
    return ({"message": "Method not allowed"}, 405)
