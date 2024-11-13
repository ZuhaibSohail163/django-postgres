# User ID for whom we are fetching legal matters
from django.core.management import BaseCommand
from django.forms import BooleanField, IntegerField

from legal_fix.models import FirmUserGroup, LegalMatter
from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg

from django.db.models.expressions import RawSQL
from django.db.models import Q, Exists, OuterRef, Subquery
from django.contrib.postgres.aggregates import ArrayAgg
import time

class Command(BaseCommand):
    help = "Inserts a new Legal Matter"

    def handle(self, *args, **options):
        try:
            # User ID for whom we are fetching legal matters
            user_id = '01JCKGJC69XMGCJPKK7ACGZYPN'

            start_time = time.time()
            # Fetch group IDs associated with the user
            group_ids = list(
                FirmUserGroup.objects.filter(
                    firm_user_ref=user_id
                ).values_list('group_ref', flat=True)
            )

            # Combine user ID and group IDs
            user_and_group_ids = [user_id] + group_ids

            # Raw SQL condition for access
            access_sql = '''
            EXISTS (
                SELECT 1 FROM jsonb_array_elements(legal_matters.acl->'acl_rules') AS rule
                WHERE (rule->'identity'->>'uid' = ANY (%s) AND rule->'identity'->>'kind' = ANY (%s))
            )
            '''

            # Annotate the LegalMatter queryset with the access condition
            legal_matters = (
                LegalMatter.objects.annotate(
                    has_access=RawSQL(
                        access_sql,
                        [user_and_group_ids, ['user', 'group']]
                    )
                )
                .filter(has_access=True)
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

            end_time = time.time()
            print(f"Execution time: {end_time - start_time:.6f} seconds")

            print('legal matters', legal_matters)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inserting subscriber: {e}"))
