from tests.constants import API_URI
from tests.utils import registration_request
from todo_api.models import User


def test_user_registrate(client, app):
    response = registration_request(client=client, api_uri=API_URI)

    with app.app_context():
        assert response.status_code == 201
        assert User.query.first().username == 'pytest_user'
        assert response.get_json().get('access_token')


def test_user_login(client, app):
    # registrate first
    registration_request(client=client, api_uri=API_URI)

    # then check whether we can log in or not
    response = client.post(f'{API_URI}/sign_in', json={
        'username': 'pytest_user',
        'password': 'pytest_password'
    })
    assert response.status_code == 200
    assert response.get_json().get('access_token')
