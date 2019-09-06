from contextlib import ExitStack
from unittest.mock import patch

from program import (
    BASE_API_URL,
    CYCLE_ID,
    get_access_token,
    get_answers,
    get_feedback_requests,
    get_questions_with_answers,
    MANAGER_ID,
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
    OAUTH_API_ENDPOINT = f'{BASE_API_URL}/oauth2/token/'

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


def test_get_feedback_requests_should_call_correct_api_endpoint():
    FEEDBACK_REQUESTS_API_ENDPOINT = f'{BASE_API_URL}/v2/feedback-cycles/{CYCLE_ID}/' \
        f'feedback-requests?managerId={MANAGER_ID}'

    with ExitStack() as stack:
        stack.enter_context(patch('program.get_access_token', return_value='access_token'))
        mock_get = stack.enter_context(patch('program.requests.get'))
        headers = {
            'Authorization': f'Bearer access_token'
        }

        get_feedback_requests(headers)

        mock_get.assert_called_once_with(FEEDBACK_REQUESTS_API_ENDPOINT, headers=headers)


def test_get_feedback_requests_should_return_feedback_requests():
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

        feedback_requests = get_feedback_requests(headers)

        assert feedback_requests == expected


def test_get_questions_with_answers_should_call_correct_api_endpoint():
    feedback_id = 'abc123'
    FEEDBACK_DETAILS_API_ENDPOINT = f'{BASE_API_URL}/v2/unified-feedback/details/' \
        f'{feedback_id}/'

    with ExitStack() as stack:
        mock_get = stack.enter_context(patch('program.requests.get'))
        headers = {
            'Authorization': f'Bearer access_token'
        }
        get_questions_with_answers(feedback_id, headers)

        mock_get.assert_called_once_with(FEEDBACK_DETAILS_API_ENDPOINT, headers=headers)


def test_get_questions_with_answers_should_return_questions_with_answers():
    feedback_id = 'abc123'

    with ExitStack() as stack:
        mock_get = stack.enter_context(patch('program.requests.get'))
        mock_get.return_value.json.return_value = expected = {
            'questionsWithAnswers': [
                {
                    'type': 'Heading',
                },
                {
                    'type': 'Question',
                    'question': '<!--MARKUP_VERSION:v3--><p>2) Are there any issue?</p>',
                    'answers': [
                        {
                            'text': '<p>I do not think he has any issue with the Pronto values.</p>'
                        },
                    ]
                },
            ]
        }
        headers = {
            'Authorization': f'Bearer access_token'
        }
        results = get_questions_with_answers(feedback_id, headers)

        assert results == expected['questionsWithAnswers']


def test_get_answers_should_get_and_extract_answers_from_response():
    expected = [
        '1) This Neutron is a good team member',
        {'3': 2, '4': 1},
        '2) Are there any issue?',
        'I do not think he has any issue with the Pronto values.',
        'He is a quiet guy.'
    ]

    questions_with_answers = [
        {
            'type': 'Heading',
        },
        {
            'type': 'LikertScale',
            'question': '<!--MARKUP_VERSION:v3--><p>1) This Neutron is a good team member</p>',
            'ratings': [
                {
                    'id': 'b10t1f',
                    'text': '4'
                },
                {
                    'id': 'i6pqp',
                    'text': '3'
                },
                {
                    'id': 'l1e67',
                    'text': '2'
                },
                {
                    'id': 'u1t0hg',
                    'text': '1'
                }
            ],
            'answers': [
                {
                    'ratingId': 'i6pqp'
                },
                {
                    'ratingId': 'i6pqp'
                },
                {
                    'ratingId': 'b10t1f'
                },
            ]
        },
        {
            'type': 'Question',
            'question': '<!--MARKUP_VERSION:v3--><p>2) Are there any issue?</p>',
            'answers': [
                {
                    'text': '<p>I do not think he has any issue with the Pronto values.</p>'
                },
                {
                    'text': '<p>He is a quiet guy.</p>'
                },
            ]
        },
    ]
    results = get_answers(questions_with_answers)

    assert results == expected
