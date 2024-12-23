from django_rdbms.models import LegalMatter, LegalMatterKind, Subscriber, Group, Firm
from django.core.management.base import BaseCommand
from django.db import connection
from .acls import acls
import json
from django.utils import timezone
import ulid



def generate_ulid():
    return str(ulid.ulid())

class Command(BaseCommand):
    help = "Inserts a new Firm"

    def add_arguments(self, parser):
        parser.add_argument("firm_id", type=str)

    def handle(self, *args, **options):
        try:
            Firm.objects.create(
                id=options['firm_id'],
                name='Homer & Sons',
                state_name='Texas',
                state_code='TX',
                email='support@homerinc.co',
                address='123 Main St. Ste 222',
                phone='333-444-5555',
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inserting subscriber: {e}"))
