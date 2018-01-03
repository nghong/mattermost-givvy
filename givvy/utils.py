from decouple import config
from .models import User, Log
import requests
import json


def check_token(token):
    MATTERMOST_TOKEN = config('MATTERMOST_TOKEN')
    if token == MATTERMOST_TOKEN:
        return True
    return False


def get_mattermost_user_from_username(username):
    url = 'https://' + config('MATTERMOST_SERVER') + '/api/v4/users/usernames'
    token = 'Bearer ' + config('MATTERMOST_REQUEST_TOKEN')
    header = {'Authorization': token}
    body = '["{username}"]'.format(username=username)

    response = requests.post(url, headers=header, data=body)
    if response.status_code == 200:
        if response.text == '[]':
            return 404, "Recipient is not found. Please recheck your command."
        # Get ID of the first user
        return 200, json.loads(response.text)[0]['id']
    return response.status_code, "Unknown error. Status code: {}".format(response.status_code)


def process_message(text):
    arguments = text.split(' ')

    if arguments[0][0] == '@':
        username = arguments[0][1:]
    else:
        username = arguments[0]
    heart = arguments[1]
    if arguments[2].lower() == 'for':
        reason = " ".join(arguments[3:])
    else:
        reason = " ".join(arguments[2:])

    return {
        'username': username,
        'heart': int(heart),
        'reason': reason
    }


def give_heart(sender, recipient, heart, reason):
    if heart > sender.quota:
        return False

    sender.quota = sender.quota - heart
    recipient.heart = recipient.heart + heart
    sender.save()
    recipient.save()

    create_log(sender, "Gave {recipient} {heart}❤. You're left with {quota} this month.".format(
        recipient=recipient.username,
        heart=heart,
        quota=sender.quota
    ))
    create_log(recipient, "Received {heart}❤ from {sender}.".format(
        heart=heart,
        sender=sender.username
    ))

    return True


def create_log(user, message):
    return Log.objects.create(user=user, message=message)
