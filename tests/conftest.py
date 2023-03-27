import pytest

from todo_api import create_app, db

API_URI = 'http://localhost:8080/todo_api/v1.0'


@pytest.fixture()
def app():
    app = create_app(database_uri='sqlite://', testing=True)

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def user_token(client, app):
    res = client.post(f'{API_URI}/sign_up', json={
        'username': 'pytest_user',
        'password': 'pytest_password'
    })
    return res.get_json()['access_token']


@pytest.fixture()
def user_header(user_token):
    headers = {
        'Authorization': f'Bearer {user_token}'
    }
    return headers
