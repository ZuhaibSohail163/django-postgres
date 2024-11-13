# User ID for whom we are fetching legal matters
from django.core.management import BaseCommand

from legal_fix.models import FirmUserGroup, LegalMatter
from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg

user_id = '01JCG3Z954GTYM2MMN5ETG8R6B'

class Command(BaseCommand):
    help = "Inserts a new Legal Matter"

    def handle(self, *args, **options):
        try:
            from django.db.models import Q, Exists, OuterRef, Subquery
            from django.contrib.postgres.aggregates import ArrayAgg

            # User ID for whom we are fetching legal matters
            user_id = '01JBF46Q61PXCE1BGHZFXVMYV9'

            # Subquery to check if any group IDs related to the user exist in acl_acl_rules
            group_ids_subquery = FirmUserGroup.objects.filter(
                firm_user_ref_id=user_id
            ).values_list('group_ref_id', flat=True)

            # Build the condition for group access
            # group_access_condition = Exists(
            #     LegalMatter.objects.filter(
            #         pk=OuterRef('pk'),
            #         acl_acl_rules_contains__identity__uid__in=group_ids_subquery
            #     )
            # )

            # Build the condition for user access
            # user_access_condition = Q(
            #     acl_acl_rules_contains=[{'identity': {'uid': user_id, 'kind': 'user'}}]
            # )

            # Query the LegalMatter model
            legal_matters = (
                LegalMatter.objects
                # .annotate(
                #     intake_data_refs=ArrayAgg('legalmatterintakedata__intake_form_id', distinct=True)
                # )
                # .filter(user_access_condition | group_access_condition)
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
            self.stderr.write(self.style.ERROR(f"Error inserting subscriber: {e}"))
