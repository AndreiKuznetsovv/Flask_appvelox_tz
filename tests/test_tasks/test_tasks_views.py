from tests.constants import API_URI
from tests.utils import post_task_request


def test_get_user_tasks_JWT(client, user_header):
    response = client.get(f'{API_URI}/tasks',
                          headers=user_header)

    assert response.status_code == 200
    assert 'tasks' in response.get_json().keys()


def test_get_user_tasks_FAKE_JWT(client):
    response = client.get(f'{API_URI}/tasks',
                          headers={'Authorization': f'Bearer FAKE JWT'})

    assert response.status_code == 422
    assert response.get_json() == {'msg': "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'"}


def test_post_user_tasks(client, user_header):
    response = client.post(f'{API_URI}/tasks',
                           headers=user_header,
                           json={'title': 'pytest_title',
                                 'text': 'pytest_text',
                                 'completion_date': '2023-03-27'
                                 }
                           )
    assert response.status_code == 201
    assert response.get_json() == {'title': 'pytest_title',
                                   'text': 'pytest_text',
                                   'completion_date': '2023-03-27',
                                   'done': False,
                                   }


def test_update_task_state(client, user_header):
    post_task_request(client=client, user_header=user_header, api_uri=API_URI)
    response = client.put(f'{API_URI}/tasks/1',
                          headers=user_header,
                          json={'done': 'True'})
    assert response.status_code == 200
    assert response.get_json()['done'] == True


def test_delete_task(client, user_header):
    post_task_request(client=client, user_header=user_header, api_uri=API_URI)
    response = client.delete(f'{API_URI}/tasks/1',
                             headers=user_header)
    assert response.status_code == 200
    assert response.get_json()['delete_flag'] == 0
