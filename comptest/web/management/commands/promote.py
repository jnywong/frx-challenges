from argparse import ArgumentParser

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "username", help="Name of existing user to promote as superuser"
        )

    def handle(self, *args, **options):
        username = options["username"]
        user = User.objects.filter(username=username).get()
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
