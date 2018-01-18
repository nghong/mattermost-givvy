from .models import User, Log
from config.settings.base import *
import requests
import json


def check_token(token):
    if token == MATTERMOST_GIVE_TOKEN:
        return True
    return False


def post_message(text, botname="Eva", channel="test-site", icon_url=""):
    url = 'https://' + MATTERMOST_HOST + '/hooks/' + MATTERMOST_WEBHOOK
    msg = {
        "username": botname,
        "channel": channel,
        "icon_url": icon_url,
        "text": text
    }
    requests.post(url, json=msg)


def get_mattermost_user_from_username(username):
    url = 'https://' + MATTERMOST_HOST + '/api/v4/users/usernames'
    token = 'Bearer ' + MATTERMOST_REQUEST_TOKEN
    header = {'Authorization': token}
    body = '["{username}"]'.format(username=username)

    response = requests.post(url, headers=header, data=body)
    if response.status_code == 200:
        if response.text == '[]':
            return 404, "There is no user with username {username}. Please recheck your command.".format(username=username)
        # Get ID of the first user
        return 200, json.loads(response.text)[0]['id']
    return response.status_code, "Unknown error. Status code: {}".format(response.status_code)


def process_message(text):
    arguments = text.split(' ')

    if len(arguments) < 2:
        return {
            'error': 'Your syntax is invalid, please recheck it and try again.'
        }

    try:
        heart = int(arguments[1])
    except ValueError:
        return {
            'error': 'Number of heart must be a positive integer, please recheck it and try again.'
        }

    if arguments[0][0] == '@':
        username = arguments[0][1:]
    else:
        username = arguments[0]

    if arguments[2].lower() == 'for':
        reason = " ".join(arguments[3:])
    else:
        reason = " ".join(arguments[2:])

    return {
        'username': username,
        'heart': heart,
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
