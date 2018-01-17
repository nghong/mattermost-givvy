import environ
import requests

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from contact.models import Contact
from givvy.models import User
from givvy.views import response_message
from givvy.utils import get_mattermost_user_from_username


env = environ.Env()


@csrf_exempt
def contact_request(request):
    token = request.POST['token']
    contact_token = env('MATTERMOST_CONTACT_TOKEN', default='')
    if token != contact_token:
        return(HttpResponse(content="You don't have permission to view this page.", status=401))

    user, created = User.objects.get_or_create(
        pk=request.POST['user_id'],
        defaults={'username': request.POST['user_name']}
    )

    # If there is no argument
    if request.POST['text'] == '':
        contact, created = Contact.objects.get_or_create(user=user)
        msg = (
            "Your current contact info:\n"
            "* Phone: " + contact.phone + "\n"
            "* Email: " + contact.email + "\n"
            "In case you want to add or overide your contact. "
            "Use `/contact add phone <phone number>` or "
            "`/contact add email <email address>`."
        )
        return response_message(msg)

    arguments = request.POST['text'].split(' ')

    if len(arguments) <= 1:
        if arguments[0][0] == '@':
            username = arguments[0][1:]
        else:
            username = arguments[0]

        status, response = get_mattermost_user_from_username(username)

        if status == 200:
            target, created = User.objects.get_or_create(
                pk=response,
                defaults={'username': username}
            )
            target_contact, created = Contact.objects.get_or_create(user=target)
            msg = (
                "@" + username + " contact info:\n"
                "* Phone: " + target_contact.phone + "\n"
                "* Email: " + target_contact.email + "\n"
            )
            return response_message(msg)
        elif status == 404:
            return response_message(response)
        else:
            return response_message(response)
