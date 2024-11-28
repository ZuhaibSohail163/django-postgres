from django_rdbms.models import Subscriber
from django.core.management.base import BaseCommand
from django.db import connection
from .acls import acls
import json
from django.utils import timezone
import ulid

def generate_ulid():
    return str(ulid.ulid())

class Command(BaseCommand):
    help = "Inserts a new subscriber"

    def add_arguments(self, parser):
        parser.add_argument("subscriber_id", type=str)

    def handle(self, *args, **options):
        try:
            subscriber_acls = acls["subscribers"].replace("{subscriber_id}", "01JD0BB5RN4J80W3795V430ZDS")
            sub = Subscriber.objects.create(
                id=options['subscriber_id'],
                last_name='Doe',
                gender='Male',
                last_updated_timestamp=timezone.now(),
                email='john.doe1@example.com',
                subscription_active=True,
                roles=['subscriber', 'editor'],
                phone='123-456-7890',
                first_name='John',
                date_of_birth='1990-01-01',
                middle_name='A.',
                acl=json.loads(subscriber_acls)
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inserting subscriber: {e}"))
