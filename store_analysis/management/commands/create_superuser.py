from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction


class Command(BaseCommand):
    help = 'Create a superuser for production deployment'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='saeed', help='Username for superuser')
        parser.add_argument('--email', default='saeed@chidmano.ir', help='Email for superuser')
        parser.add_argument('--password', default='Saeed33124', help='Password for superuser')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        try:
            with transaction.atomic():
                # Check if user already exists
                if User.objects.filter(username=username).exists():
                    self.stdout.write(
                        self.style.WARNING(f'User {username} already exists')
                    )
                    return

                # Create superuser
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created superuser: {username}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
