from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import process_message, check_token, get_mattermost_user_from_username, create_log, give_heart
from .models import User


def response_message(msg, channel="", msg_type="ephemeral"):
    response = {
        "username": "Eva",
        "text": msg
    }

    if channel:
        response["channel"] = channel
        return JsonResponse(response)

    response["response_type"] = msg_type
    return JsonResponse(response)

@csrf_exempt
def handle_mattermost_request(request):
    """
    Handle requests sent from Mattermost.
    1. Check token
    2. Get all necessary arguments
    3. Check sender != recipient
    4. Try to give heart from sender to recipient
    5. Return response
    """

    # Check token
    # (This is not secure but mattermost request sends token like this.)
    token = request.POST['token']
    if not(check_token(token)):
        return(HttpResponse(content="You don't have permission to view this page.", status=401))

    # If there is no argument
    if request.POST['text'] == '':
        sender, created = User.objects.get_or_create(
            pk=request.POST['user_id'],
            defaults={'username': request.POST['user_name']}
        )
        msg = "You currently have {heart}❤.\nYou can give other team members {quota}❤ this month.".format(
            heart=sender.heart,
            quota=sender.quota
        )
        return response_message(msg)

    # Get arguments
    params = process_message(request.POST['text'])
    if 'error' in params:
        return response_message(params['error'])
    status, response = get_mattermost_user_from_username(params['username'])
    if status == 200:
        recipient_id = response
    elif status == 404:
        return response_message(response)
    else:
        return response_message(response)

    sender, created = User.objects.get_or_create(
        pk=request.POST['user_id'],
        defaults={'username': request.POST['user_name']}
    )
    recipient, created = User.objects.get_or_create(
        pk=recipient_id,
        defaults={'username': params['username']}
    )

    # Don't allow sender giving heart to themselves
    if (sender.mattermost_id == recipient.mattermost_id) or (sender.username == recipient.username):
        return response_message("You cannot give heart to yourself.")

    # Try to give heart
    given = give_heart(sender, recipient, params['heart'], params['reason'])
    if given:
        msg = "You've just given @{username} {heart}❤ of your heart. You're left with {quota}.".format(
            username=params['username'],
            heart=params['heart'],
            quota=sender.quota
        )
        response_message(
            "{sender} has just given {recipient} {heart}❤ for {reason}.".format(
                sender=sender.username,
                recipient=recipient.username,
                heart=params['heart'],
                reason=params['reason']
            ), channel="test-site"
        )
    else:
        msg = "Action failed. You've just tried to give a number of hearts exceeding your quota this month."

    return response_message(msg)
