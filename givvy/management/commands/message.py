from django.core.management.base import BaseCommand
from givvy.utils import post_message


class Command(BaseCommand):
    help = "A simple messenger."

    def add_arguments(self, parser):
        parser.add_argument(
            'message', nargs='+',
            help='What is the message?')
        parser.add_argument(
            '--channel', default='test-site',
            help='What is the channel to message?')
        parser.add_argument(
            '--name', default='Siri',
            help='What is the name of the bot?')

    def handle(self, *args, **options):
        post_message(" ".join(options['message']),
                     botname=options['name'],
                     channel=options['channel'])
