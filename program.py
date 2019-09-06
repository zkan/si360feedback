import os

import requests


AUTH_BASIC_TOKEN = os.environ.get('AUTH_BASIC_TOKEN')
SI_USERNAME = os.environ.get('SI_USERNAME')
SI_PASSWORD = os.environ.get('SI_PASSWORD')
BASE_API_URL = 'https://www.small-improvements.com/api'

CYCLE_ID = 'YUG98Peo6q98yqU25sytlA'
MANAGER_ID = 'DLwCz1IxRVSuFU6y565Psw'
OAUTH_API_ENDPOINT = f'{BASE_API_URL}/oauth2/token/'
FEEDBACK_REQUESTS_API_ENDPOINT = f'{BASE_API_URL}/v2/feedback-cycles/{CYCLE_ID}/' \
    f'feedback-requests?managerId={MANAGER_ID}'


def get_access_token(username, password, auth_basic_token):
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
    r = requests.post(OAUTH_API_ENDPOINT, data=payload, headers=headers)
    data = r.json()

    return data.get('access_token')


def get_feedback_requests(headers):
    requests.get(FEEDBACK_REQUESTS_API_ENDPOINT, headers=headers)


if __name__ == '__main__':
    access_token = get_access_token(SI_USERNAME, SI_PASSWORD, AUTH_BASIC_TOKEN)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    r = requests.get(FEEDBACK_REQUESTS_API_ENDPOINT, headers=headers)
    data = r.json()

    for each in data:
        print(each['reviewee']['name'])

        feedback_id = each['id']
        FEEDBACK_DETAILS_API_ENDPOINT = f'{BASE_API_URL}/v2/unified-feedback/details/' \
            f'{feedback_id}/'
        r = requests.get(FEEDBACK_DETAILS_API_ENDPOINT, headers=headers)
        data = r.json()
        questions_with_answers = data['questionsWithAnswers']
        for question in questions_with_answers:
            if question['type'] == 'LikertScale':
                print(question['question'])
                final_ratings = {}
                for answer in question['answers']:
                    for rating in question['ratings']:
                        if rating['id'] == answer['ratingId']:
                            try:
                                final_ratings[rating['text']] += 1
                            except KeyError:
                                final_ratings[rating['text']] = 1

                print(final_ratings)

            elif question['type'] == 'Question':
                print(question['question'])
                for answer in question['answers']:
                    print(answer['text'])
