from legal_fix.models import LegalMatter, LegalMatterKind, Subscriber
from django.core.management.base import BaseCommand
from django.db import connection
from .acls import acls
import json
from django.utils import timezone
import ulid

def generate_ulid():
    return str(ulid.ulid())

class Command(BaseCommand):
    help = "Inserts a new Legal Matter"

    def handle(self, *args, **options):
        try:
            lm_acls = acls["legal_matters"].replace("{subscriber_id}", '01JBF46Q60T3A7VSJ7T2KGWRT2')
            subscriber_instance = Subscriber.objects.get(id='01JCG3Z954GTYM2MMN5ETG8R6B')
            lm_kind_instance = LegalMatterKind.objects.get(id='01JCK4NPMTC2G4881V5HTKD4KC')
            LegalMatter.objects.create(
                id=generate_ulid(),
                status='Pending',
                kind_ref=lm_kind_instance,
                created_timestamp=timezone.now(),
                subscriber_ref=subscriber_instance,
                acl=json.loads(lm_acls)
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inserting subscriber: {e}"))
