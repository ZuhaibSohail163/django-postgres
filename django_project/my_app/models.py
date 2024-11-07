from django.db import models

class Subscriber(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50, null=True, blank=True)
    last_updated_timestamp = models.DateTimeField()
    email = models.EmailField(unique=True)
    subscription_active = models.BooleanField()
    roles = models.JSONField(default=list)
    phone = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'subscribers'


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    roles = models.JSONField(default=list)
    name = models.CharField(max_length=255)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'groups'

us_counties
class Firm(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    state_name = models.CharField(max_length=255)
    state_code = models.CharField(max_length=2)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'firms'


class FirmGroup(models.Model):
    id = models.AutoField(primary_key=True)
    firm_id = models.ForeignKey(Firm, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'firm_groups'


class FirmUser(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    last_updated_timestamp = models.DateTimeField()
    number_of_assigning_legal_matters = models.IntegerField(default=0)
    number_of_assigned_legal_matters = models.IntegerField(default=0)
    roles = models.JSONField(default=list)
    phone = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    firm_ref = models.ForeignKey(Firm, on_delete=models.CASCADE)
    _type = models.CharField(max_length=50, default="FirmUser")
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'firm_users'


class Label(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = 'labels'


class FirmUserLabel(models.Model):
    id = models.AutoField(primary_key=True)
    firm_user_id = models.ForeignKey(FirmUser, on_delete=models.CASCADE)
    label_id = models.ForeignKey(Label, on_delete=models.CASCADE)

    class Meta:
        db_table = 'firm_user_labels'


class FirmUserGroup(models.Model):
    id = models.AutoField(primary_key=True)
    firm_user_id = models.ForeignKey(FirmUser, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'firm_user_groups'


class Invite(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_timestamp = models.DateTimeField()
    last_updated_timestamp = models.DateTimeField()
    email = models.EmailField()
    firm_user_ref = models.ForeignKey(FirmUser, null=True, blank=True, on_delete=models.CASCADE, related_name='invites_as_user')
    expires_at = models.DateTimeField()
    firm_admin_ref = models.ForeignKey(FirmUser, on_delete=models.CASCADE, related_name='invites_as_admin')
    user_name = models.CharField(max_length=255)
    firm_ref = models.ForeignKey(Firm, on_delete=models.CASCADE)
    firm_groups = models.JSONField(default=list)
    withdrawn_timestamp = models.DateTimeField(null=True, blank=True)
    withdrawn_reason = models.CharField(max_length=255, null=True, blank=True)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'invites'


class IntakeForm(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.JSONField()
    last_updated_timestamp = models.DateTimeField()
    created_timestamp = models.DateTimeField()
    form_version = models.CharField(max_length=255)

    class Meta:
        db_table = 'intake_forms'


class CheckoutSession(models.Model):
    id = models.AutoField(primary_key=True)
    expires_at = models.DateTimeField()
    created = models.DateTimeField()
    amount_subtotal = models.FloatField()
    amount_total = models.FloatField()
    url = models.URLField()
    subscriber_ref = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'checkout_sessions'


class LegalMatterKind(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    intake_form = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    products = models.JSONField(default=list)

    class Meta:
        db_table = 'legal_matter_kinds'


class LegalMatter(models.Model):
    id = models.AutoField(primary_key=True)
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
    rejection_reason = models.CharField(max_length=255, null=True, blank=True)
    withdraw_reason = models.CharField(max_length=255, null=True, blank=True)
    referral_rejected_reason = models.CharField(max_length=255, null=True, blank=True)
    rating = models.IntegerField(default=0)
    kind_ref = models.ForeignKey(LegalMatterKind, on_delete=models.CASCADE)
    subscriber_ref = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    assigned_lawyer_ref = models.ForeignKey(FirmUser, null=True, blank=True, on_delete=models.CASCADE)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'legal_matters'


class LegalMatterIntakeData(models.Model):
    id = models.AutoField(primary_key=True)
    legal_matter_id = models.ForeignKey(LegalMatter, on_delete=models.CASCADE)
    intake_form_id = models.ForeignKey(IntakeForm, on_delete=models.CASCADE)

    class Meta:
        db_table = 'legal_matter_intake_data'


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_timestamp = models.DateTimeField()
    last_updated_timestamp = models.DateTimeField()
    completed_timestamp = models.DateTimeField(null=True, blank=True)
    tracked_minutes = models.IntegerField(default=0)
    assigned_to_firm_user_ref = models.ForeignKey(FirmUser, null=True, blank=True, on_delete=models.CASCADE, related_name='tasks_assigned')
    assigned_to_subscriber_ref = models.ForeignKey(Subscriber, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    assigned_timestamp = models.DateTimeField()
    created_by_ref = models.ForeignKey(FirmUser, on_delete=models.CASCADE, related_name='tasks_created')
    legal_matter_ref = models.ForeignKey(LegalMatter, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    charge_type = models.CharField(max_length=50, null=True, blank=True)
    charge_reason = models.CharField(max_length=255, null=True, blank=True)
    charge_amount = models.FloatField(default=0)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'tasks'


class CalendarEvent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    last_updated_timestamp = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    legal_matter_ref = models.ForeignKey(LegalMatter, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'calendar_events'


class CalendarEventParticipant(models.Model):
    id = models.AutoField(primary_key=True)
    calendar_event_id = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    participant_firm_user_ref = models.ForeignKey(FirmUser, null=True, blank=True, on_delete=models.CASCADE)
    participant_subscriber_ref = models.ForeignKey(Subscriber, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'calendar_event_participants'


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    note = models.TextField()
    created_timestamp = models.DateTimeField()
    last_updated_timestamp = models.DateTimeField()
    updated_by_ref = models.ForeignKey(FirmUser, null=True, blank=True, on_delete=models.CASCADE, related_name='notes_updated')
    created_by_ref = models.ForeignKey(FirmUser, null=True, blank=True, on_delete=models.CASCADE, related_name='notes_created')
    legal_matter_ref = models.ForeignKey(LegalMatter, on_delete=models.CASCADE)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'notes'


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_timestamp = models.DateTimeField()
    updated_timestamp = models.DateTimeField()
    md5_hash = models.CharField(max_length=32)
    size = models.IntegerField()
    full_path = models.CharField(max_length=1024)
    type = models.CharField(max_length=50)
    legal_matter_ref = models.ForeignKey(LegalMatter, on_delete=models.CASCADE)
    acl = models.JSONField(default=dict)

    class Meta:
        db_table = 'documents'


class DocumentLink(models.Model):
    id = models.AutoField(primary_key=True)
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    url = models.URLField()

    class Meta:
        db_table = 'documentlink'
