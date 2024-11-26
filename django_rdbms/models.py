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
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'subscribers'
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="subscribers_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="subscribers_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="subscribers_acl_roles_idx",
            ),
        ]

# Group model
class Group(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    roles = ArrayField(
        models.TextField(),
        blank=True,  # Optional: allows the array to be empty
        null=False    # Optional: allows the array to be null
    )
    name = models.CharField(max_length=255)
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'groups'
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="groups_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="groups_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="groups_acl_roles_idx",
            ),
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
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'firms'
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="firms_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="firms_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="firms_acl_roles_idx",
            ),
        ]

# FirmGroup model
class FirmGroup(models.Model):
    firm_ref = models.ForeignKey('Firm', on_delete=models.CASCADE, db_column='firm_ref')
    group_ref = models.ForeignKey('Group', on_delete=models.CASCADE, db_column='group_ref')

    class Meta:
        db_table = 'firm_groups'
        constraints = [
            models.UniqueConstraint(fields=['firm_ref', 'group_ref'], name='firm_group_pk'),
        ]

# FirmUser model
class FirmUser(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    last_updated_timestamp = models.DateTimeField()
    number_of_assigning_legal_matters = models.IntegerField(db_default=0)
    number_of_assigned_legal_matters = models.IntegerField(db_default=0)
    roles = ArrayField(
        models.TextField(),
        blank=True,  # Optional: allows the array to be empty
        null=False    # Optional: allows the array to be null
    )
    phone = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    firm_ref = models.ForeignKey('Firm', on_delete=models.RESTRICT, db_column='firm_ref')
    _type = models.CharField(max_length=50)
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'firm_users'
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="firm_users_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="firm_users_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="firm_users_acl_roles_idx",
            ),
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
    firm_user_ref = models.ForeignKey('FirmUser', on_delete=models.CASCADE, db_column='firm_user_ref')
    label_ref = models.ForeignKey('Label', on_delete=models.CASCADE, db_column='label_ref')

    class Meta:
        db_table = 'firm_user_labels'
        constraints = [
            models.UniqueConstraint(fields=['firm_user_ref', 'label_ref'], name='firm_user_label_pk')
        ]

# FirmUserGroup model
class FirmUserGroup(models.Model):
    firm_user_ref = models.ForeignKey('FirmUser', on_delete=models.CASCADE, db_column='firm_user_ref')
    group_ref = models.ForeignKey('Group', on_delete=models.CASCADE, db_column='group_ref')

    class Meta:
        db_table = 'firm_user_groups'
        constraints = [
            models.UniqueConstraint(fields=['firm_user_ref', 'group_ref'], name='firm_user_group_pk')
        ]

# Invite model
class Invite(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    user_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_timestamp = models.DateTimeField()
    last_updated_timestamp = models.DateTimeField()
    email = models.CharField(max_length=255)
    firm_user_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.SET_NULL, related_name='invites_as_user', db_column='firm_user_ref')
    expires_at = models.DateTimeField()
    firm_admin_ref = models.ForeignKey('FirmUser', on_delete=models.CASCADE, related_name='invites_as_admin', db_column='firm_admin_ref')
    user_name = models.CharField(max_length=255)
    firm_ref = models.ForeignKey('Firm', on_delete=models.CASCADE, db_column='firm_ref')
    firm_groups = ArrayField(
        models.TextField(),
        blank=True,  # Optional: allows the array to be empty
        null=False    # Optional: allows the array to be null
    )
    withdrawn_timestamp = models.DateTimeField(null=True, blank=True)
    withdrawn_reason = models.TextField(null=True, blank=True)
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'invites'
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="invites_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="invites_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="invites_acl_roles_idx",
            ),
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

# CheckoutSession model
class CheckoutSession(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    expires_at = models.DateTimeField()
    created = models.DateTimeField()
    amount_subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.TextField()
    subscriber_ref = models.ForeignKey('Subscriber', on_delete=models.CASCADE, db_column='subscriber_ref')
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'checkout_sessions'
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="checkout_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="checkout_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="checkout_acl_roles_idx",
            ),
        ]

# LegalMatterKind model
class LegalMatterKind(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    category = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    intake_form = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    products = ArrayField(
        models.TextField(),  # Field type for the array elements
        default=list,  # Python default for empty array
        db_default="{}"  # Ensures it generates as text[] with the proper default
    )

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
    rating = models.IntegerField(db_default=0)
    kind_ref = models.ForeignKey('LegalMatterKind', on_delete=models.RESTRICT, db_column='kind_ref')
    subscriber_ref = models.ForeignKey('Subscriber', on_delete=models.RESTRICT, db_column='subscriber_ref')
    assigned_lawyer_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.RESTRICT, db_column='assigned_lawyer_ref')
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'legal_matters'
        indexes = [
            models.Index(fields=['created_timestamp'], name='lm_created_timestamp_idx'),
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="lm_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="lm_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="lm_acl_roles_idx",
            ),
        ]

# LegalMatterIntakeData model
class LegalMatterIntakeData(models.Model):
    legal_matter_ref = models.ForeignKey('LegalMatter', on_delete=models.CASCADE, db_column='legal_matter_ref')
    intake_form_ref = models.ForeignKey('IntakeForm', on_delete=models.CASCADE, db_column='intake_form_ref')

    class Meta:
        db_table = 'legal_matter_intake_data'
        constraints = [
            models.UniqueConstraint(fields=['legal_matter_ref', 'intake_form_ref'], name='legal_matter_intake_data_pk')
        ]

# Task model
class Task(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    name = models.CharField(max_length=255)
    created_timestamp = models.DateTimeField()
    last_updated_timestamp = models.DateTimeField()
    completed_timestamp = models.DateTimeField(null=True, blank=True)
    tracked_minutes = models.IntegerField(db_default=0)
    assigned_to_firm_user_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.RESTRICT, related_name='tasks_assigned_to_firm_user', db_column='assigned_to_firm_user_ref')
    assigned_to_subscriber_ref = models.ForeignKey('Subscriber', null=True, blank=True, on_delete=models.RESTRICT, related_name='tasks_assigned_to_subscriber', db_column='assigned_to_subscriber_ref')
    status = models.CharField(max_length=50)
    assigned_timestamp = models.DateTimeField()
    created_by_ref = models.ForeignKey('FirmUser', on_delete=models.RESTRICT, related_name='tasks_created_by', db_column='created_by_ref')
    legal_matter_ref = models.ForeignKey('LegalMatter', on_delete=models.CASCADE, db_column='legal_matter_ref')
    description = models.TextField(null=True, blank=True)
    charge_type = models.CharField(max_length=20, null=True, blank=True)
    charge_reason = models.TextField(null=True, blank=True)
    charge_amount = models.DecimalField(max_digits=10, decimal_places=2, db_default=0)
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'tasks'
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="tasks_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="tasks_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="tasks_acl_roles_idx",
            ),
            models.Index(fields=['created_timestamp'], name='tasks_created_timestamp_idx'),
            models.Index(fields=['legal_matter_ref'], name='tasks_legal_matter_ref_idx'),
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
    legal_matter_ref = models.ForeignKey('LegalMatter', on_delete=models.CASCADE, db_column='legal_matter_ref')
    description = models.TextField(null=True, blank=True)
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'calendar_events'
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="events_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="events_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="events_acl_roles_idx",
            ),
            models.Index(fields=['last_updated_timestamp'], name='last_updated_timestamp_idx'),
            models.Index(fields=['legal_matter_ref'], name='legal_matter_ref_idx'),
        ]

# CalendarEventParticipant model
class CalendarEventParticipant(models.Model):
    id = models.BigAutoField(primary_key=True)
    calendar_event_ref = models.ForeignKey('CalendarEvent', on_delete=models.CASCADE, db_column='calendar_event_ref')
    participant_firm_user_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.RESTRICT, db_column='participant_firm_user_ref')
    participant_subscriber_ref = models.ForeignKey('Subscriber', null=True, blank=True, on_delete=models.RESTRICT, db_column='participant_subscriber_ref')

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
    updated_by_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.SET_NULL, related_name='notes_updated_by', db_column='updated_by_ref')
    created_by_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.SET_NULL, related_name='notes_created_by', db_column='created_by_ref')
    legal_matter_ref = models.ForeignKey('LegalMatter', on_delete=models.CASCADE, db_column='legal_matter_ref')
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'notes'
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="notes_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="notes_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="notes_acl_roles_idx",
            ),
            models.Index(fields=['created_timestamp'], name='notes_created_timestamp_idx'),
            models.Index(fields=['legal_matter_ref'], name='notes_legal_matter_ref_idx'),
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
    created_by_firm_user_ref = models.ForeignKey('FirmUser', null=True, blank=True, on_delete=models.RESTRICT, related_name='documents_created_by_firm_user', db_column='created_by_firm_user_ref')
    created_by_subscriber_ref = models.ForeignKey('Subscriber', null=True, blank=True, on_delete=models.RESTRICT, related_name='documents_created_by_subscriber', db_column='created_by_subscriber_ref')
    legal_matter_ref = models.ForeignKey('LegalMatter', on_delete=models.CASCADE, db_column='legal_matter_ref')
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'documents'
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="docs_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="docs_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="docs_acl_roles_idx",
            ),
            models.Index(fields=['created_timestamp'], name='docs_created_timestamp_idx'),
            models.Index(fields=['legal_matter_ref'], name='documents_legal_matter_ref_idx'),
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
    document_ref = models.ForeignKey('Document', on_delete=models.CASCADE, db_column='document_ref')
    task_ref = models.ForeignKey('Task', on_delete=models.CASCADE, db_column='task_ref')

    class Meta:
        db_table = 'task_documents'
        constraints = [
            models.UniqueConstraint(fields=['document_ref', 'task_ref'], name='task_documents_pk')
        ]

# LegalMatterAudit model
class LegalMatterAudit(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_timestamp = models.DateTimeField()
    details = models.TextField()
    legal_matter_ref = models.ForeignKey('LegalMatter', on_delete=models.CASCADE, db_column='legal_matter_ref')

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
    requirements_errors = ArrayField(
        models.TextField(),  # Field type for the array elements
        default=list,  # Python default for empty array
        db_default="{}"  # Ensures it generates as text[] with the proper default
    )
    requirements_pending_verification = ArrayField(
        models.TextField(),  # Field type for the array elements
        default=list,  # Python default for empty array
        db_default="{}"  # Ensures it generates as text[] with the proper default
    )
    requirements_current_deadline = models.DateTimeField(null=True, blank=True)
    requirements_disabled_reason = models.TextField(null=True, blank=True)
    firm_ref = models.ForeignKey('Firm', on_delete=models.CASCADE, db_column='firm_ref')
    payouts_enabled = models.BooleanField()
    charges_enabled = models.BooleanField()
    _type = models.CharField(max_length=50)
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'payment_processor_accounts'
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="pma_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="pma_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="pma_acl_roles_idx",
            ),
        ]

# SubscriptionDetail model
class SubscriptionDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    last_invoice_id = models.CharField(max_length=100)
    last_invoice_status = models.CharField(max_length=50)
    billing_cycle_anchor = models.DateTimeField()
    last_event_timestamp = models.DateTimeField()
    last_event_id = models.CharField(max_length=100)
    subscriber_ref = models.ForeignKey('Subscriber', on_delete=models.CASCADE, db_column='subscriber_ref')
    subscription_status = models.CharField(max_length=50)
    customer_id = models.CharField(max_length=100)
    current_period_end = models.DateTimeField()
    _type = models.CharField(max_length=50)
    subscription_id = models.CharField(max_length=100, unique=True)
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

    class Meta:
        db_table = 'subscription_details'
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="sub_details_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="sub_details_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="sub_details_acl_roles_idx",
            ),
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
    subscription_detail_ref = models.ForeignKey('SubscriptionDetail', on_delete=models.CASCADE, db_column='subscription_detail_ref')

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
    labels = ArrayField(
        models.TextField(),  # Field type for the array elements
        default=list,  # Python default for empty array
        db_default="{}"  # Ensures it generates as text[] with the proper default
    )
    created_timestamp = models.DateTimeField()
    severity = models.CharField(max_length=50)
    firm_user_ref = models.ForeignKey(
        'FirmUser', on_delete=models.RESTRICT, null=True, blank=True, db_column='firm_user_ref'
    )
    subscriber_ref = models.ForeignKey(
        'Subscriber', on_delete=models.RESTRICT, null=True, blank=True, db_column='subscriber_ref'
    )
    message = models.TextField()
    acl = models.JSONField(default=dict, db_default='{}')
    acl_flat = models.JSONField(default=dict, db_default='{}')

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
        indexes = [
            GinIndex(
                OpClass(models.F("acl_flat__entity_get"), name="jsonb_path_ops"),
                name="messages_acl_get_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__entity_list"), name="jsonb_path_ops"),
                name="messages_acl_list_idx",
            ),
            GinIndex(
                OpClass(models.F("acl_flat__role_identities"), name="jsonb_path_ops"),
                name="messages_acl_roles_idx",
            ),
        ]
