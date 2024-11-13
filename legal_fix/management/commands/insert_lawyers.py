from legal_fix.models import Subscriber, FirmUser, Firm
from django.core.management.base import BaseCommand
from django.db import connection
from .acls import acls
import json
from django.utils import timezone
import ulid

def generate_ulid():
    return str(ulid.ulid())

class Command(BaseCommand):
    help = "Inserts a new Lawyer"

    def handle(self, *args, **options):
        try:
            firm_instance = Firm.objects.get(id='01JCKGH149S4MFARWT96A3D4X4')
            FirmUser.objects.create(
                id=generate_ulid(),
                last_name='Doe',
                last_updated_timestamp=timezone.now(),
                email='lawyer.doe@example.com',
                number_of_assigning_legal_matters=1,
                number_of_assigned_legal_matters=2,
                roles=['LawyerUser', 'Manager'],
                phone='123-456-7890',
                first_name='Lawyer',
                firm_ref=firm_instance,
                _type='LawyerUser',
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inserting Firm user: {e}"))
