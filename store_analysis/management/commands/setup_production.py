from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import connection
import os


class Command(BaseCommand):
    help = 'Setup production database with migrations and superuser'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='saeed', help='Username for superuser')
        parser.add_argument('--email', default='saeed@chidmano.ir', help='Email for superuser')
        parser.add_argument('--password', default='Saeed33124', help='Password for superuser')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        try:
            # Check if database exists
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='django_migrations';")
                tables_exist = cursor.fetchone() is not None

            if not tables_exist:
                self.stdout.write("📊 Creating database tables...")
                call_command('makemigrations')
                call_command('migrate', '--noinput')
                self.stdout.write(self.style.SUCCESS('✅ Database tables created successfully'))
            else:
                self.stdout.write("📊 Running migrations...")
                call_command('migrate', '--noinput')
                self.stdout.write(self.style.SUCCESS('✅ Migrations completed'))

            # Create superuser
            if not User.objects.filter(username=username).exists():
                self.stdout.write(f"👤 Creating superuser: {username}")
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f'✅ Superuser {username} created successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ Superuser {username} already exists'))

            # Collect static files
            self.stdout.write("📁 Collecting static files...")
            call_command('collectstatic', '--noinput')
            self.stdout.write(self.style.SUCCESS('✅ Static files collected'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error in setup: {e}'))
            raise
