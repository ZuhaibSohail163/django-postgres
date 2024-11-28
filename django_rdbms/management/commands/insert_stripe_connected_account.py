
from django.core.management.base import BaseCommand
from django.db import connection

from django_rdbms.models import Capabilities, Requirements, StripeConnectedAccount
from .acls import acls
import json
from django.utils import timezone
import ulid
  
def generate_ulid():
  return str(ulid.ulid())
  
class Command(BaseCommand):
  help = "Inserts a new Stripe Connected Account"

  def handle(self, *args, **options):
    try:
      capabilities_instance = Capabilities.objects.create(
        capabilities_card_payments="active",
        capabilities_transfers="active",
      )

      # Step 2: Create a Requirements instance
      requirements_instance = Requirements.objects.create(
        requirements_current_deadline="2024-12-31T23:59:59Z",
        requirements_disabled_reason="None",
        requirements_pending_verification=["document_1", "document_2"],
        requirements_errors=[],
      )

      print("instance", requirements_instance)
      StripeConnectedAccount.objects.create(
        id=generate_ulid(),
        stripe_type='express',
        stripe_email='support@homerinc.co',
        stripe_details_submitted=True,
        stripe_charges_enabled=True,
        stripe_payouts_enabled=True,
        capabilities=capabilities_instance,
        requirements=requirements_instance,
      )
    except Exception as e:

      self.stderr.write(self.style.ERROR(f"Error inserting Stripe Connected Account: {e}"))