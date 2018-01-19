import environ
from django.core.management.base import BaseCommand
from givvy.models import User


env = environ.Env()


class Command(BaseCommand):
    help = "Reset quota of all users."

    def handle(self, *args, **options):
        User.objects.all().update(quota=env.int('GIVVY_QUOTA', default=100))
