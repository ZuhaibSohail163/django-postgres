from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.postgres.indexes import GinIndex, OpClass


# Subscriber model
class Subscriber(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50, null=True, blank=True)
    last_updated_timestamp = models.DateTimeField()
    email = models.CharField(max_length=255, unique=True)
    subscription_active = models.BooleanField()
    roles = ArrayField(
        models.TextField(),
        blank=True,  # Optional: allows the array to be empty
        null=False    # Optional: allows the array to be null
    )
    phone = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'subscribers'
        indexes = [
            GinIndex(fields=['acl'], name='subscribers_acl_idx'),
            # GinIndex(
            #     name='subscribers_acl_rules_idx',
            #     fields=['acl'],
            #     opclasses=['jsonb_path_ops'],
            #     expressions=['(acl ->> \'acl_rules\')']
            # ),c
            # GinIndex(
            #     OpClass('(acl ->> \'acl_rules\')', name="jsonb_path_ops"),
            #     name="subscribers_acl_rules_idx",
            # ),
        # GinIndex(fields=['acl.acl_rules'], name='subscribers_acl_rules_idx'),
            # models.Index(name='subscribers_acl_rules_idx', fields=[], expressions=[models.F('acl').key('acl_rules')], opclasses=['gin'])
        ]

# Group model
class Group(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    roles = models.JSONField()
    name = models.CharField(max_length=255)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'groups'
        indexes = [
            # models.Index(fields=['acl'], name='groups_acl_idx', opclasses=['gin']),
            GinIndex(fields=['acl'], name='groups_acl_idx'),
            # models.Index(name='groups_acl_rules_idx', fields=[], expressions=[models.F('acl').key('acl_rules')], opclasses=['gin'])
        ]

# Firm model
class Firm(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    name = models.CharField(max_length=255)
    state_name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=2)
    email = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, null=True, blank=True)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'firms'
        indexes = [
            # models.Index(fields=['acl'], name='firms_acl_idx', opclasses=['gin']),
            GinIndex(fields=['acl'], name='firms_acl_idx'),
            # models.Index(name='firms_acl_rules_idx', fields=[], expressions=[models.F('acl').key('acl_rules')], opclasses=['gin'])
        ]

# FirmGroup model
class FirmGroup(models.Model):
    firm_id = models.ForeignKey('Firm', on_delete=models.CASCADE)
    group_id = models.ForeignKey('Group', on_delete=models.CASCADE)

    class Meta:
        db_table = 'firm_groups'
        constraints = [
            models.UniqueConstraint(fields=['firm_id', 'group_id'], name='firm_group_pk')
        ]

# FirmUser model
class FirmUser(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    last_updated_timestamp = models.DateTimeField()
    number_of_assigning_legal_matters = models.IntegerField(default=0)
    number_of_assigned_legal_matters = models.IntegerField(default=0)
    roles = models.JSONField()
    phone = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    firm_ref = models.ForeignKey('Firm', on_delete=models.RESTRICT)
    _type = models.CharField(max_length=50)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'firm_users'
        indexes = [
            # models.Index(fields=['acl'], name='firm_users_acl_idx', opclasses=['gin'])
            GinIndex(fields=['acl'], name='firm_users_acl_idx'),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(_type__in=['FirmUser', 'LawyerUser']),
                name='firm_users__type_check'
            )
        ]


# Label model
class Label(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    category = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = 'labels'

# FirmUserLabel model
class FirmUserLabel(models.Model):
    firm_user_id = models.ForeignKey('FirmUser', on_delete=models.CASCADE)
    label_id = models.ForeignKey('Label', on_delete=models.CASCADE)

    class Meta:
        db_table = 'firm_user_labels'
        constraints = [
            models.UniqueConstraint(fields=['firm_user_id', 'label_id'], name='firm_user_label_pk')
        ]

# FirmUserGroup model
class FirmUserGroup(models.Model):
    firm_user_id = models.ForeignKey('FirmUser', on_delete=models.CASCADE)
    group_id = models.ForeignKey('Group', on_delete=models.CASCADE)

    class Meta:
        db_table = 'firm_user_groups'
        constraints = [
            models.UniqueConstraint(fields=['firm_user_id', 'group_id'], name='firm_user_group_pk')
        ]

# Invite model
class Invite(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    user_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_timestamp = models.DateTimeField()
    last_updated_timestamp = models.DateTimeField()
    email = models.CharField(max_length=255)
    firm_user_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.SET_NULL, related_name='invites_as_user')
    expires_at = models.DateTimeField()
    firm_admin_ref = models.ForeignKey('FirmUser', on_delete=models.CASCADE, related_name='invites_as_admin')
    user_name = models.CharField(max_length=255)
    firm_ref = models.ForeignKey('Firm', on_delete=models.CASCADE)
    firm_groups = models.JSONField()
    withdrawn_timestamp = models.DateTimeField(null=True, blank=True)
    withdrawn_reason = models.TextField(null=True, blank=True)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'invites'
        indexes = [
            # models.Index(fields=['acl'], name='invites_acl_idx', opclasses=['gin']),
            GinIndex(fields=['acl'], name='invites_acl_idx'),
            # models.Index(name='invites_acl_rules_idx', fields=[], expressions=[models.F('acl').key('acl_rules')], opclasses=['gin'])
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(user_type__in=['FirmUser', 'LawyerUser']),
                name='invites_user_type_check'
            )
        ]

# IntakeForm model
class IntakeForm(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    data = models.JSONField()
    last_updated_timestamp = models.DateTimeField()
    created_timestamp = models.DateTimeField()
    form_version = models.CharField(max_length=255)

    class Meta:
        db_table = 'intake_forms'
        indexes = [
            # models.Index(fields=['data'], name='intake_forms_data_idx', opclasses=['gin'])
            GinIndex(fields=['data'], name='intake_forms_data_idx'),
        ]

# CheckoutSession model
class CheckoutSession(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    expires_at = models.DateTimeField()
    created = models.DateTimeField()
    amount_subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.TextField()
    subscriber_ref = models.ForeignKey('Subscriber', on_delete=models.CASCADE)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'checkout_sessions'
        indexes = [
            # models.Index(fields=['acl'], name='checkout_sessions_acl_idx', opclasses=['gin']),
            GinIndex(fields=['acl'], name='checkout_sessions_acl_idx'),
            # models.Index(name='checkout_sessions_acl_rules_idx', fields=[], expressions=[models.F('acl').key('acl_rules')], opclasses=['gin'])
        ]

# LegalMatterKind model
class LegalMatterKind(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    category = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    intake_form = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    products = models.JSONField(default=list)

    class Meta:
        db_table = 'legal_matter_kinds'


# LegalMatter model
class LegalMatter(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    created_timestamp = models.DateTimeField()
    status = models.CharField(max_length=50)
    assigned_timestamp = models.DateTimeField(null=True, blank=True)
    accepted_timestamp = models.DateTimeField(null=True, blank=True)
    referral_timestamp = models.DateTimeField(null=True, blank=True)
    referral_accepted_timestamp = models.DateTimeField(null=True, blank=True)
    referral_rejected_timestamp = models.DateTimeField(null=True, blank=True)
    closed_timestamp = models.DateTimeField(null=True, blank=True)
    canceled_timestamp = models.DateTimeField(null=True, blank=True)
    withdrawn_timestamp = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    withdraw_reason = models.TextField(null=True, blank=True)
    referral_rejected_reason = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=0)
    kind_ref = models.ForeignKey('LegalMatterKind', on_delete=models.RESTRICT)
    subscriber_ref = models.ForeignKey('Subscriber', on_delete=models.RESTRICT)
    assigned_lawyer_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.RESTRICT)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'legal_matters'
        indexes = [
            # models.Index(fields=['acl'], name='legal_matters_acl_idx', opclasses=['gin']),
            GinIndex(fields=['acl'], name='legal_matters_acl_idx'),
            models.Index(fields=['created_timestamp'], name='lm_created_timestamp_idx'),
            # models.Index(name='legal_matters_acl_rules_idx', fields=[], expressions=[models.F('acl').key('acl_rules')], opclasses=['gin'])
        ]

# LegalMatterIntakeData model
class LegalMatterIntakeData(models.Model):
    legal_matter_id = models.ForeignKey('LegalMatter', on_delete=models.CASCADE)
    intake_form_id = models.ForeignKey('IntakeForm', on_delete=models.CASCADE)

    class Meta:
        db_table = 'legal_matter_intake_data'
        constraints = [
            models.UniqueConstraint(fields=['legal_matter_id', 'intake_form_id'], name='legal_matter_intake_data_pk')
        ]

# Task model
class Task(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    name = models.CharField(max_length=255)
    created_timestamp = models.DateTimeField()
    last_updated_timestamp = models.DateTimeField()
    completed_timestamp = models.DateTimeField(null=True, blank=True)
    tracked_minutes = models.IntegerField(default=0)
    assigned_to_firm_user_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.RESTRICT, related_name='tasks_assigned_to_firm_user')
    assigned_to_subscriber_ref = models.ForeignKey('Subscriber', null=True, blank=True, on_delete=models.RESTRICT, related_name='tasks_assigned_to_subscriber')
    status = models.CharField(max_length=50)
    assigned_timestamp = models.DateTimeField()
    created_by_ref = models.ForeignKey('FirmUser', on_delete=models.RESTRICT, related_name='tasks_created_by')
    legal_matter_ref = models.ForeignKey('LegalMatter', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    charge_type = models.CharField(max_length=20, null=True, blank=True)
    charge_reason = models.TextField(null=True, blank=True)
    charge_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'tasks'
        indexes = [
            # models.Index(fields=['acl'], name='tasks_acl_idx', opclasses=['gin']),
            GinIndex(fields=['acl'], name='tasks_acl_idx'),
            models.Index(fields=['created_timestamp'], name='tasks_created_timestamp_idx'),
            models.Index(fields=['legal_matter_ref'], name='tasks_legal_matter_ref_idx'),
            # models.Index(name='tasks_acl_rules_idx', fields=[], expressions=[models.F('acl').key('acl_rules')], opclasses=['gin'])
        ]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(assigned_to_firm_user_ref__isnull=False, assigned_to_subscriber_ref__isnull=True) |
                    models.Q(assigned_to_firm_user_ref__isnull=True, assigned_to_subscriber_ref__isnull=False)
                ),
                name='tasks_check'
            )
        ]

# CalendarEvent model
class CalendarEvent(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    last_updated_timestamp = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    legal_matter_ref = models.ForeignKey('LegalMatter', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'calendar_events'
        indexes = [
            # models.Index(fields=['acl'], name='calendar_events_acl_idx', opclasses=['gin']),
            GinIndex(fields=['acl'], name='calendar_events_acl_idx'),
            models.Index(fields=['last_updated_timestamp'], name='last_updated_timestamp_idx'),
            models.Index(fields=['legal_matter_ref'], name='legal_matter_ref_idx'),
            # models.Index(name='calendar_events_acl_rules_idx', fields=[], expressions=[models.F('acl').key('acl_rules')], opclasses=['gin'])
        ]

# CalendarEventParticipant model
class CalendarEventParticipant(models.Model):
    id = models.BigAutoField(primary_key=True)
    calendar_event_id = models.ForeignKey('CalendarEvent', on_delete=models.CASCADE)
    participant_firm_user_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.RESTRICT)
    participant_subscriber_ref = models.ForeignKey('Subscriber', null=True, blank=True, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'calendar_event_participants'
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(participant_firm_user_ref__isnull=False, participant_subscriber_ref__isnull=True) |
                    models.Q(participant_firm_user_ref__isnull=True, participant_subscriber_ref__isnull=False)
                ),
                name='calendar_event_participants_check'
            )
        ]

# Note model
class Note(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    note = models.TextField()
    created_timestamp = models.DateTimeField()
    last_updated_timestamp = models.DateTimeField()
    updated_by_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.SET_NULL, related_name='notes_updated_by')
    created_by_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.SET_NULL, related_name='notes_created_by')
    legal_matter_ref = models.ForeignKey('LegalMatter', on_delete=models.CASCADE)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'notes'
        indexes = [
            # models.Index(fields=['acl'], name='notes_acl_idx', opclasses=['gin']),
            GinIndex(fields=['acl'], name='notes_acl_idx'),
            models.Index(fields=['created_timestamp'], name='notes_created_timestamp_idx'),
            models.Index(fields=['legal_matter_ref'], name='notes_legal_matter_ref_idx'),
            # models.Index(name='notes_acl_rules_idx', fields=[], expressions=[models.F('acl').key('acl_rules')], opclasses=['gin'])
        ]

# Document model
class Document(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    name = models.CharField(max_length=255)
    created_timestamp = models.DateTimeField()
    updated_timestamp = models.DateTimeField()
    md5_hash = models.CharField(max_length=32)
    size = models.IntegerField()
    full_path = models.TextField()
    created_by_firm_user_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.RESTRICT, related_name='documents_created_by_firm_user')
    created_by_subscriber_ref = models.ForeignKey('Subscriber', null=True, blank=True, on_delete=models.RESTRICT, related_name='documents_created_by_subscriber')
    legal_matter_ref = models.ForeignKey('LegalMatter', on_delete=models.CASCADE)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'documents'
        indexes = [
            # models.Index(fields=['acl'], name='documents_acl_idx', opclasses=['gin']),
            GinIndex(fields=['acl'], name='documents_acl_idx'),
            models.Index(fields=['created_timestamp'], name='created_timestamp_idx'),
            models.Index(fields=['legal_matter_ref'], name='documents_legal_matter_ref_idx'),
            # models.Index(name='documents_acl_rules_idx', fields=[], expressions=[models.F('acl').key('acl_rules')], opclasses=['gin'])
        ]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(created_by_firm_user_ref__isnull=False, created_by_subscriber_ref__isnull=True) |
                    models.Q(created_by_firm_user_ref__isnull=True, created_by_subscriber_ref__isnull=False)
                ),
                name='documents_check'
            )
        ]

# TaskDocument model
class TaskDocument(models.Model):
    document_id = models.ForeignKey('Document', on_delete=models.CASCADE)
    task_id = models.ForeignKey('Task', on_delete=models.CASCADE)

    class Meta:
        db_table = 'task_documents'
        constraints = [
            models.UniqueConstraint(fields=['document_id', 'task_id'], name='task_documents_pk')
        ]

# LegalMatterAudit model
class LegalMatterAudit(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_timestamp = models.DateTimeField()
    details = models.TextField()
    legal_matter_ref = models.ForeignKey('LegalMatter', on_delete=models.CASCADE)

    class Meta:
        db_table = 'legal_matter_audit'

# PaymentProcessorAccount model
class PaymentProcessorAccount(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=255)
    created = models.DateTimeField()
    details_submitted = models.BooleanField()
    type = models.CharField(max_length=50)
    capabilities_card_payments = models.CharField(max_length=50)
    capabilities_transfers = models.CharField(max_length=50)
    requirements_errors = models.JSONField(default=list)
    requirements_pending_verification = models.JSONField(default=list)
    requirements_current_deadline = models.DateTimeField(null=True, blank=True)
    requirements_disabled_reason = models.TextField(null=True, blank=True)
    firm_ref = models.ForeignKey('Firm', on_delete=models.CASCADE)
    payouts_enabled = models.BooleanField()
    charges_enabled = models.BooleanField()
    _type = models.CharField(max_length=50)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'payment_processor_accounts'
        indexes = [
            # models.Index(fields=['acl'], name='payment_processor_acl_idx', opclasses=['gin']),
            GinIndex(fields=['acl'], name='payment_processor_acl_idx'),
            # models.Index(name='payment_processor_accounts_acl_rules_idx', fields=[], expressions=[models.F('acl').key('acl_rules')], opclasses=['gin'])
        ]

# SubscriptionDetail model
class SubscriptionDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    last_invoice_id = models.CharField(max_length=100)
    last_invoice_status = models.CharField(max_length=50)
    billing_cycle_anchor = models.DateTimeField()
    last_event_timestamp = models.DateTimeField()
    last_event_id = models.CharField(max_length=100)
    subscriber_ref = models.ForeignKey('Subscriber', on_delete=models.CASCADE)
    subscription_status = models.CharField(max_length=50)
    customer_id = models.CharField(max_length=100)
    current_period_end = models.DateTimeField()
    _type = models.CharField(max_length=50)
    subscription_id = models.CharField(max_length=100, unique=True)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'subscription_details'
        indexes = [
            # models.Index(fields=['acl'], name='subscription_details_acl_idx', opclasses=['gin']),
            GinIndex(fields=['acl'], name='subscription_details_acl_idx'),
            # models.Index(name='subscription_details_acl_rules_idx', fields=[], expressions=[models.F('acl').key('acl_rules')], opclasses=['gin'])
        ]

# SubscriptionProduct model
class SubscriptionProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=20)
    price_id = models.CharField(max_length=255)
    price_lookup_key = models.TextField(null=True, blank=True)
    price_recurring_interval = models.CharField(max_length=10, null=True, blank=True)
    price_unit_amount = models.IntegerField()
    subscription_detail_ref = models.ForeignKey('SubscriptionDetail', on_delete=models.CASCADE)

    class Meta:
        db_table = 'subscription_products'

# USCity model
class USCity(models.Model):
    id = models.BigAutoField(primary_key=True)
    city = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)
    city_lower = models.CharField(max_length=100)
    county_name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=2)

    class Meta:
        db_table = 'us_cities'

# USCounty model
class USCounty(models.Model):
    id = models.BigAutoField(primary_key=True)
    county_fips = models.CharField(max_length=5, unique=True)
    state_name = models.CharField(max_length=100)
    county_name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=2)

    class Meta:
        db_table = 'us_counties'

# USState model
class USState(models.Model):
    id = models.BigAutoField(primary_key=True)
    state_name = models.CharField(max_length=100, unique=True)
    state_code = models.CharField(max_length=2, unique=True)

    class Meta:
        db_table = 'us_states'

# UserMessage model
class UserMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    labels = models.JSONField(default=list)
    created_timestamp = models.DateTimeField()
    severity = models.CharField(max_length=50)
    firm_user_ref = models.ForeignKey(
        'FirmUser', on_delete=models.RESTRICT, null=True, blank=True
    )
    subscriber_ref = models.ForeignKey(
        'Subscriber', on_delete=models.RESTRICT, null=True, blank=True
    )
    message = models.TextField()
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'user_messages'
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(firm_user_ref__isnull=False, subscriber_ref__isnull=True) |
                    models.Q(firm_user_ref__isnull=True, subscriber_ref__isnull=False)
                ),
                name='user_messages_check'
            )
        ]