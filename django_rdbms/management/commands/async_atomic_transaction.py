from django_rdbms.models import FirmGroup, Firm, Group
from django.core.management.base import BaseCommand
from django.db import connection
from .acls import acls
import json
from django.utils import timezone
import ulid
from django.db import transaction
from asgiref.sync import sync_to_async

import asyncio

def generate_ulid():
    return str(ulid.ulid())

class Command(BaseCommand):
    help = "Demonstrate an atomic transaction"

    def handle(self, *args, **kwargs):
        # Run the asynchronous function within the synchronous handle method
        asyncio.run(self.async_handle())
      
    async def async_handle(self):
        try:
            # Use sync_to_async to wrap the synchronous transaction.atomic block
            await sync_to_async(self.create_records_in_transaction)()

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))


    def create_records_in_transaction(self):
        try:
            group_id = generate_ulid()
            firm_id = generate_ulid()

            with transaction.atomic():
              # Create a Group instance
              group = Group.objects.create(
                  id=group_id,
                  label='Main Group',
                  roles=['admin', 'user'],
                  name='Example Group'
              )
              print("Group created:", group)

              # Create a Firm instance
              firm = Firm.objects.create(
                  id=firm_id,
                  name='Example Firm',
                  state_name='California',
                  state_code='CA',
                  email='contact@examplefirm.com',
                  address='123 Example Street, Example City, CA 90001',
                  phone='123-456-7890'
              )
              print("Firm created:", firm)

              # raise Exception("bad")

              # Create a FirmGroup instance linking the Firm and Group
              firm_group = FirmGroup.objects.create(
                  firm_ref=firm,
                  group_ref=group
              )
              print("FirmGroup created:", firm_group)
            
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error during atomic transaction: {e}"))
            print(e)
