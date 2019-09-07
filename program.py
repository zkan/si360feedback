import os

import requests


SI_USERNAME = os.environ.get('SI_USERNAME')
SI_PASSWORD = os.environ.get('SI_PASSWORD')
AUTH_BASIC_TOKEN = os.environ.get('AUTH_BASIC_TOKEN')
BASE_API_URL = 'https://www.small-improvements.com/api'
CYCLE_ID = 'YUG98Peo6q98yqU25sytlA'
MANAGER_ID = 'DLwCz1IxRVSuFU6y565Psw'
REVIEW_ID = 'aUme0DmBwRht6T8iubT4gw'


def strip_markup_comment(text):
    return text.replace('<!--MARKUP_VERSION:v3-->', '')


def strip_p(text):
    return text.replace('<p>', '').replace('</p>', '')


def get_access_token(username, password, auth_basic_token):
    OAUTH_API_ENDPOINT = f'{BASE_API_URL}/oauth2/token/'
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
    response = requests.post(OAUTH_API_ENDPOINT, data=payload, headers=headers)
    data = response.json()

    return data['access_token']


def get_feedback_requests(headers):
    FEEDBACK_REQUESTS_API_ENDPOINT = f'{BASE_API_URL}/v2/feedback-cycles/{CYCLE_ID}/' \
        f'feedback-requests?managerId={MANAGER_ID}'
    response = requests.get(FEEDBACK_REQUESTS_API_ENDPOINT, headers=headers)
    data = response.json()

    return data


def get_questions_with_answers(feedback_id, headers):
    FEEDBACK_DETAILS_API_ENDPOINT = f'{BASE_API_URL}/v2/unified-feedback/details/' \
        f'{feedback_id}/'
    response = requests.get(FEEDBACK_DETAILS_API_ENDPOINT, headers=headers)
    data = response.json()

    return data['questionsWithAnswers']


def get_answers(questions_with_answers):
    results = []
    for question in questions_with_answers:
        if question['type'] == 'Heading':
            continue

        results.append(strip_p(strip_markup_comment(question['question'])))
        if question['type'] == 'LikertScale':
            final_ratings = {}
            for answer in question['answers']:
                for rating in question['ratings']:
                    if rating['id'] == answer['ratingId']:
                        try:
                            final_ratings[rating['text']] += 1
                        except KeyError:
                            final_ratings[rating['text']] = 1

            results.append(final_ratings)

        elif question['type'] == 'Question':
            for answer in question['answers']:
                results.append(answer['text'])

    return results


def get_assessment(review_id, headers):
    ASSESSMENT_API_ENDPOINT = f'{BASE_API_URL}/v2/assessment?reviewId={review_id}'
    response = requests.get(ASSESSMENT_API_ENDPOINT, headers=headers)
    data = response.json()

    return data[0]


def get_self_review(reviewee):
    results = []
    for answer in reviewee['answers']:
        if answer['type'] == 'TEXT':
            description = answer['questionPayload']['description']
            results.append(strip_p(strip_markup_comment((description))))
            if 'text' in answer['answerPayload']:
                results.append(strip_markup_comment((answer['answerPayload']['text'])))

    return results


if __name__ == '__main__':
    access_token = get_access_token(SI_USERNAME, SI_PASSWORD, AUTH_BASIC_TOKEN)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    data = get_feedback_requests(headers)

    for each in data:
        print(each['reviewee']['name'])
        feedback_id = each['id']
        questions_with_answers = get_questions_with_answers(feedback_id, headers)
        results = get_answers(questions_with_answers)
        for result in results:
            print(result)

    print('-' * 10)

    reviewee = get_assessment(REVIEW_ID, headers)

    print('Self-Review')
    results = get_self_review(reviewee)
    for result in results:
        print(result)
