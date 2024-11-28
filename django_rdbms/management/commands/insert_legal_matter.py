from django_rdbms.models import LegalMatter, LegalMatterKind, Subscriber
from django.core.management.base import BaseCommand
from django.db import connection
from .acls import acls, acls_flat
import json
from django.utils import timezone
import ulid

def generate_ulid():
    return str(ulid.ulid())

class Command(BaseCommand):
    help = "Inserts a new Legal Matter"

    def add_arguments(self, parser):
        parser.add_argument("subscriber_id", type=str)
        parser.add_argument("group_id", type=str)
        parser.add_argument("lawyer_id", type=str)
        parser.add_argument("legal_matter_kind_id", type=str)

    def handle(self, *args, **options):
        subscriber_id = options["subscriber_id"]
        group_id = options["group_id"]
        lawyer_id = options["lawyer_id"]
        legal_matter_kind_id = options["legal_matter_kind_id"]

        try:
            lm_acls = acls["legal_matters"].replace("{subscriber_id}", subscriber_id).replace("{group_id}", group_id).replace("{lawyer_id}", lawyer_id)
            lm_acls_flat = acls_flat["legal_matters"].replace("{subscriber_id}", subscriber_id).replace("{group_id}", group_id).replace("{lawyer_id}", lawyer_id)
            subscriber_instance = Subscriber.objects.get(id=subscriber_id)
            lm_kind_instance = LegalMatterKind.objects.get(id=legal_matter_kind_id)
            LegalMatter.objects.create(
                id=generate_ulid(),
                status='UNASSIGNED',
                kind_ref=lm_kind_instance,
                created_timestamp=timezone.now(),
                subscriber_ref=subscriber_instance,
                acl=json.loads(lm_acls),
                acl_flat=json.loads(lm_acls_flat)
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inserting subscriber: {e}"))
