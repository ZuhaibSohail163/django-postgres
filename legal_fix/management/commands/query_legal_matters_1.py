# User ID for whom we are fetching legal matters
from django.core.management import BaseCommand

from legal_fix.models import FirmUserGroup, LegalMatter
from django.db.models import Q
import time

user_id = '01JCKGJC69XMGCJPKK7ACGZYPN'

class Command(BaseCommand):
    help = "Inserts a new Legal Matter"

    def handle(self, *args, **options):
        try:
            # Fetch group IDs associated with the user
            # User ID for whom we are fetching legal matters

            # Fetch group IDs associated with the user
            start_time = time.time()
            group_ids = list(
                FirmUserGroup.objects.filter(firm_user_ref=user_id).values_list('group_ref', flat=True)
            )
            # print(group_ids)

            # Build the conditions to check in the acl_rules
            conditions = Q(acl__acl_rules__contains=[{'identity': {'uid': user_id, 'kind': 'user'}}])
            for group_id in group_ids:
                conditions |= Q(acl__acl_rules__contains=[{'identity': {'uid': group_id, 'kind': 'group'}}])

            # Query the LegalMatter model
            legal_matters = (
                LegalMatter.objects
                .filter(conditions)
                .order_by('-created_timestamp')[:10]
                .values(
                    'id', 'kind_ref', 'status', 'subscriber_ref', 'created_timestamp',
                    'assigned_timestamp', 'accepted_timestamp', 'referral_timestamp',
                    'referral_accepted_timestamp', 'referral_rejected_timestamp',
                    'referral_rejected_reason', 'closed_timestamp', 'canceled_timestamp',
                    'withdrawn_timestamp', 'rejection_reason', 'withdraw_reason',
                    'rating', 'assigned_lawyer_ref'
                )
            )
            print('legal matters', legal_matters)

            end_time = time.time()
            print(f"Execution time: {end_time - start_time:.6f} seconds")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error fetching legal matters: {e}"))
