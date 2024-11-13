from legal_fix.models import LegalMatter, LegalMatterKind, Subscriber, Group
from django.core.management.base import BaseCommand
from django.db import connection
from .acls import acls
import json
from django.utils import timezone
import ulid



def generate_ulid():
    return str(ulid.ulid())

class Command(BaseCommand):
    help = "Inserts a new Group"

    def handle(self, *args, **options):
        try:

            Group.objects.create(
                id=generate_ulid(),
                label='legal-matter-assigners',
                roles=['legalMatters.assigner', 'groups.manager'],
                name='Miguel & Sons Assigners',
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inserting subscriber: {e}"))
