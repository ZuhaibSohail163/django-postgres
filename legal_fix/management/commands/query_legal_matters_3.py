# User ID for whom we are fetching legal matters
from django.core.management import BaseCommand
from django.forms import BooleanField

from legal_fix.models import FirmUserGroup, LegalMatter
from django.db.models import Q, Exists, OuterRef, Subquery
from django.contrib.postgres.aggregates import ArrayAgg

from django.db.models.expressions import RawSQL

class Command(BaseCommand):
    help = "Inserts a new Legal Matter"

    def handle(self, *args, **options):
        try:

            # User ID for whom we are fetching legal matters
            user_id = '01JCKGFF0XAAWTWWCJD4SNMPDR'

            # Raw SQL condition for group access
            group_access_sql = '''
            EXISTS (
                SELECT 1 FROM jsonb_array_elements(acl->'acl_rules') AS rule
                WHERE (rule->'identity'->>'uid' IN (
                    SELECT group_ref FROM firm_user_groups WHERE firm_user_ref = %s
                ) AND rule->'identity'->>'kind' = 'group')
            )
            '''

            # Raw SQL condition for user access
            user_access_sql = '''
            EXISTS (
                SELECT 1 FROM jsonb_array_elements(acl->'acl_rules') AS rule
                WHERE rule->'identity'->>'uid' = %s AND rule->'identity'->>'kind' = 'user'
            )
            '''

            # Query the LegalMatter model
            legal_matters = (
                LegalMatter.objects
                .annotate(
                    user_access=RawSQL(user_access_sql, (user_id,)),
                    group_access=RawSQL(group_access_sql, (user_id,)),
                )
                .filter(Q(user_access=True) | Q(group_access=True))
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
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inserting legal matter: {e}"))