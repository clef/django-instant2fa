from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Seed the db with a superuser if it does not already exist'

    def handle(self, *args, **options):
        try:
            admin = User.objects.get(username='admin')
            self.stdout.write(self.style.SUCCESS('Admin is already seeded.'))
        except ObjectDoesNotExist:
            User.objects.create_superuser('admin', 'admin@example.com', 'password')
            self.stdout.write(self.style.SUCCESS('Admin successfuly created.'))
