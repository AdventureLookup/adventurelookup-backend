from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Creates a superuser account with admin:admin credentials.'

    def handle(self, *args, **options):
        try:
            User.objects.create_superuser('admin', 'admin@adventurelookup.com', 'admin')
        except IntegrityError as e:
            raise CommandError("User admin already exists.")

        except Exception as e:
            raise CommandError("Couldn't create admin user. Reason:", e)

        self.stdout.write(self.style.SUCCESS('Successfully created admin user with password "admin"'))
