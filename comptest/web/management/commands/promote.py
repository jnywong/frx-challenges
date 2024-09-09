from argparse import ArgumentParser

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "usernames",
            nargs="+",
            help="""
            List of existing users to promote as superusers,
            e.g., user1 user2 user3
            """,
        )

    def handle(self, *args, **options):
        usernames = options["usernames"]
        for username in usernames:
            try:
                user = User.objects.filter(username=username).get()
                user.is_staff = True
                user.is_admin = True
                user.is_superuser = True
                user.save()
                print(self.style.SUCCESS(f"Successfully promoted {username}"))
            except User.DoesNotExist:
                print(self.style.ERROR(f"User {username} does not exist"))
