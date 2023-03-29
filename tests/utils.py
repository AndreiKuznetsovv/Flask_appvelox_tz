API_URI = 'http://localhost:8080/todo_api/v1.0'

def registration_request(client, api_uri):
    return client.post(f'{api_uri}/sign_up', json={
        'username': 'pytest_user',
        'password': 'pytest_password'
    })


def post_task_request(client, user_header, api_uri):
    return client.post(f'{api_uri}/tasks',
                       headers=user_header,
                       json={'title': 'pytest_title',
                             'text': 'pytest_text',
                             'completion_date': '2023-03-27'
                             }
                       )