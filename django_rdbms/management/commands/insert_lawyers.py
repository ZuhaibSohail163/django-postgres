from django_rdbms.models import Subscriber, FirmUser, Firm
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

    def add_arguments(self, parser):
        parser.add_argument("lawyer_id", type=str)
        parser.add_argument("firm_id", type=str)

    def handle(self, *args, **options):
        try:
            firm_instance = Firm.objects.get(id=options['firm_id'])
            FirmUser.objects.create(
                id=options['lawyer_id'],
                last_name='Doe',
                last_updated_timestamp=timezone.now(),
                email=f"lawyer.doe{options['lawyer_id']}@example.com",
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
