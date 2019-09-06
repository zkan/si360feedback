from contextlib import ExitStack
from unittest.mock import patch

from program import get_access_token, OAUTH_API_ENDPOINT


def test_get_access_token_should_call_correct_oauth_api_endpoint():
    username = 'kan@pronto.com'
    password = 'hellopronto'
    auth_basic_token = '12345'

    payload = {
        'grant_type': 'password',
        'username': username,
        'password': password,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth_basic_token}',
        'User-Agent': 'small_improvements_bot_app',
    }

    with ExitStack() as stack:
        mock_post = stack.enter_context(patch('program.requests.post'))

        get_access_token(username, password, auth_basic_token)

        mock_post.assert_called_once_with(OAUTH_API_ENDPOINT, data=payload, headers=headers)
