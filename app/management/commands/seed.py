from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seed the db with a superuser if it does not already exist'

    def handle(self, *args, **options):
        admin = User.objects.get(username='admin')
        if admin:
            self.stdout.write(self.style.SUCCESS('Admin is already seeded.'))
        else:
            User.objects.create_superuser('admin', 'admin@example.com', 'password')
            self.stdout.write(self.style.SUCCESS('Admin successfuly created.'))
