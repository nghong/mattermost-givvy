import environ
import requests

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from contact.models import Contact
from givvy.models import User
from givvy.views import response_message


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
