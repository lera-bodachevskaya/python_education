from django.core.management.base import BaseCommand

from ...views import update_all_cities


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        update_all_cities()
