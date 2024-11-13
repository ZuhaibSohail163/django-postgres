from legal_fix.models import LegalMatterKind
from django.core.management.base import BaseCommand
from django.db import connection
from .acls import acls
import json
from django.utils import timezone
import ulid

def generate_ulid():
    return str(ulid.ulid())

class Command(BaseCommand):
    help = "Inserts a new Legal Matter Kind"

    def handle(self, *args, **options):
        try:
            LegalMatterKind.objects.create(
                id=generate_ulid(),
                category='Elder Law',
                description='some description',
                intake_form='General_Legal_Matter',
                name='Consult with Attorney',
                products=['prod_PjjJuLJkKKnoeV', 'prod_QWsZuHUCe5M21a'],
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inserting subscriber: {e}"))
