from django_rdbms.models import FirmUserGroup, Group, FirmUser
from django.core.management.base import BaseCommand

import ulid

def generate_ulid():
    return str(ulid.ulid())

class Command(BaseCommand):
    help = "Inserts a new firm user group"

    def add_arguments(self, parser):
        parser.add_argument("lawyer_id", type=str)
        parser.add_argument("group_id", type=str)

    def handle(self, *args, **options):
        try:
            firm_user_instance = FirmUser.objects.get(id=options['lawyer_id'])
            group_instance = Group.objects.get(id=options['group_id'])
            FirmUserGroup.objects.create(
                firm_user_ref=firm_user_instance,
                group_ref=group_instance,
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inserting firm user group: {e}"))
