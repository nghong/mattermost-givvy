import environ

from django.http import HttpResponse
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

    contact, created = Contact.objects.get_or_create(user=user)

    # If there is no argument
    if request.POST['text'] == '':
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

    if arguments[0].lower() == 'add' and len(arguments) >= 3:
        if arguments[1].lower() == 'phone' and arguments[2]:
            contact.phone = arguments[2]
        if arguments[1].lower() == 'email' and arguments[2]:
            contact.email = arguments[2]
        contact.save()
        return response_message("Your contact info has been updated.")

    if len(arguments) <= 1 and arguments[0].lower() != 'add':
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

    return response_message("Your syntax is invalid. Please recheck and try again.")
