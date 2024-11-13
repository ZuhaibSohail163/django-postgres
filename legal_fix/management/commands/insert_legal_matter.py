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
            lm_acls = acls["legal_matters"].replace("{subscriber_id}", '01JCKGFF0XAAWTWWCJD4SNMPDR')
            subscriber_instance = Subscriber.objects.get(id='01JCKGFF0XAAWTWWCJD4SNMPDR')
            lm_kind_instance = LegalMatterKind.objects.get(id='01JCKGMPWN3D4RK2SNHEWMVGQ8')
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
