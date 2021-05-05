from django.core.management.base import BaseCommand
import csv
from django.contrib.auth.models import User, Group, Permission
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Creating new users'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help='File name with .csv extension, where the Log will be saved')

    def handle(self, *args, **kwargs):
        filename = kwargs['file_name']
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                username = row[2]
                password = row[1]
                email = row[3]
                user = User.objects.filter(username=row[0]).update(username=username,email=email)


        admin_group, created = Group.objects.get_or_create(name='sos_admin')
        view_user = Permission.objects.get(name='Can view whats app users')
        change_user = Permission.objects.get(name='Can change whats app users')
        admin_group.permissions.add(view_user, change_user)
        user.groups.add(admin_group)
