from contextlib import ExitStack
from unittest.mock import patch

from program import (
    get_access_token,
    get_feedback_requests,
    FEEDBACK_REQUESTS_API_ENDPOINT,
    OAUTH_API_ENDPOINT,
    strip_markup_comment,
    strip_p,
)


def test_strip_markup_comment_should_remove_markup_comment():
    expected = '<p>5) Are we OK with him</p>'

    text = '<!--MARKUP_VERSION:v3--><p>5) Are we OK with him</p>'
    result = strip_markup_comment(text)

    assert result == expected


def test_strip_p_should_remove_p_tag():
    expected = '5) Are we OK with him'

    text = '<p>5) Are we OK with him</p>'
    result = strip_p(text)

    assert result == expected


def test_get_access_token_should_call_correct_api_endpoint():
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


def test_get_access_token_should_return_access_token():
    username = 'kan@pronto.com'
    password = 'hellopronto'
    auth_basic_token = '12345'

    with ExitStack() as stack:
        mock_data = {
            'access_token': 'ACCESS_TOKEN',
            'scope': 'global',
            'token_type': 'bearer'
        }
        mock_post = stack.enter_context(patch('program.requests.post'))
        mock_post.return_value.json.return_value = mock_data

        access_token = get_access_token(username, password, auth_basic_token)

        assert access_token == 'ACCESS_TOKEN'


def test_get_feedback_requests_data_should_call_correct_api_endpoint():
    with ExitStack() as stack:
        stack.enter_context(patch('program.get_access_token', return_value='access_token'))
        mock_get = stack.enter_context(patch('program.requests.get'))
        headers = {
            'Authorization': f'Bearer access_token'
        }

        get_feedback_requests(headers)

        mock_get.assert_called_once_with(FEEDBACK_REQUESTS_API_ENDPOINT, headers=headers)


def test_get_feedback_requests_data_should_return_feedback_requests():
    with ExitStack() as stack:
        stack.enter_context(patch('program.get_access_token', return_value='access_token'))
        mock_get = stack.enter_context(patch('program.requests.get'))
        mock_get.return_value.json.return_value = expected = [
            {
                'id': 'w0s*gSmDalS6NsJDvrYpiA',
                'reviewee': {
                    'id': 'NEcSDCAXrbj0aNGKALH1mw',
                    'name': 'Alif Ruksaithong',
                }
            }
        ]

        headers = {
            'Authorization': f'Bearer access_token'
        }

        feedback_requests_data = get_feedback_requests(headers)

        assert feedback_requests_data == expected
