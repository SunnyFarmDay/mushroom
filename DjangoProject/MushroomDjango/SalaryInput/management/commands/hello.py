from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Display Hello'

    def handle(self, *args, **kwargs):
        self.stdout.write("Hello World!")