from legal_fix.models import FirmUserGroup, Group, FirmUser
from django.core.management.base import BaseCommand

import ulid

def generate_ulid():
    return str(ulid.ulid())

class Command(BaseCommand):
    help = "Inserts a new firm user group"

    def handle(self, *args, **options):
        try:
            firm_user_instance = FirmUser.objects.get(id='01JCKGJC69XMGCJPKK7ACGZYPN')
            group_instance = Group.objects.get(id='01JCKGJP1NY3DYWSZ2EAH906MF')
            FirmUserGroup.objects.create(
                # id=generate_ulid(),
                firm_user_ref=firm_user_instance,
                group_ref=group_instance,
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inserting firm user group: {e}"))
