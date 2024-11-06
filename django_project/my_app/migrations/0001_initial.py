# Generated by Django 5.1.3 on 2024-11-06 18:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_timestamp', models.DateTimeField()),
                ('updated_timestamp', models.DateTimeField()),
                ('md5_hash', models.CharField(max_length=32)),
                ('size', models.IntegerField()),
                ('full_path', models.CharField(max_length=1024)),
                ('type', models.CharField(max_length=50)),
                ('acl', models.JSONField(default=dict)),
            ],
            options={
                'db_table': 'document',
            },
        ),
        migrations.CreateModel(
            name='Firm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('state_name', models.CharField(max_length=255)),
                ('state_code', models.CharField(max_length=2)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField()),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('acl', models.JSONField(default=dict)),
            ],
            options={
                'db_table': 'firm',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('roles', models.JSONField(default=list)),
                ('name', models.CharField(max_length=255)),
                ('acl', models.JSONField(default=dict)),
            ],
            options={
                'db_table': 'group',
            },
        ),
        migrations.CreateModel(
            name='IntakeForm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.JSONField()),
                ('last_updated_timestamp', models.DateTimeField()),
                ('created_timestamp', models.DateTimeField()),
                ('form_version', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'intakeform',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'label',
            },
        ),
        migrations.CreateModel(
            name='LegalMatterKind',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('intake_form', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('products', models.JSONField(default=list)),
            ],
            options={
                'db_table': 'legalmatterkind',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('last_name', models.CharField(max_length=255)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('last_updated_timestamp', models.DateTimeField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('subscription_active', models.BooleanField()),
                ('roles', models.JSONField(default=list)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('first_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('acl', models.JSONField(default=dict)),
            ],
            options={
                'db_table': 'subscriber',
            },
        ),
        migrations.CreateModel(
            name='DocumentLink',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.URLField()),
                ('document_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.document')),
            ],
            options={
                'db_table': 'documentlink',
            },
        ),
        migrations.CreateModel(
            name='FirmUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('last_updated_timestamp', models.DateTimeField()),
                ('number_of_assigning_legal_matters', models.IntegerField(default=0)),
                ('number_of_assigned_legal_matters', models.IntegerField(default=0)),
                ('roles', models.JSONField(default=list)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('first_name', models.CharField(max_length=255)),
                ('_type', models.CharField(default='FirmUser', max_length=50)),
                ('acl', models.JSONField(default=dict)),
                ('firm_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.firm')),
            ],
            options={
                'db_table': 'firmuser',
            },
        ),
        migrations.CreateModel(
            name='FirmUserGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('firm_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.firmuser')),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.group')),
            ],
            options={
                'db_table': 'firmusergroup',
            },
        ),
        migrations.CreateModel(
            name='FirmGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('firm_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.firm')),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.group')),
            ],
            options={
                'db_table': 'firmgroup',
            },
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_type', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('created_timestamp', models.DateTimeField()),
                ('last_updated_timestamp', models.DateTimeField()),
                ('email', models.EmailField(max_length=254)),
                ('expires_at', models.DateTimeField()),
                ('user_name', models.CharField(max_length=255)),
                ('firm_groups', models.JSONField(default=list)),
                ('withdrawn_timestamp', models.DateTimeField(blank=True, null=True)),
                ('withdrawn_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('acl', models.JSONField(default=dict)),
                ('firm_admin_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites_as_admin', to='my_app.firmuser')),
                ('firm_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.firm')),
                ('firm_user_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invites_as_user', to='my_app.firmuser')),
            ],
            options={
                'db_table': 'invite',
            },
        ),
        migrations.CreateModel(
            name='FirmUserLabel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('firm_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.firmuser')),
                ('label_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.label')),
            ],
            options={
                'db_table': 'firmuserlabel',
            },
        ),
        migrations.CreateModel(
            name='LegalMatter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_timestamp', models.DateTimeField()),
                ('status', models.CharField(max_length=50)),
                ('assigned_timestamp', models.DateTimeField(blank=True, null=True)),
                ('accepted_timestamp', models.DateTimeField(blank=True, null=True)),
                ('referral_timestamp', models.DateTimeField(blank=True, null=True)),
                ('referral_accepted_timestamp', models.DateTimeField(blank=True, null=True)),
                ('referral_rejected_timestamp', models.DateTimeField(blank=True, null=True)),
                ('closed_timestamp', models.DateTimeField(blank=True, null=True)),
                ('canceled_timestamp', models.DateTimeField(blank=True, null=True)),
                ('withdrawn_timestamp', models.DateTimeField(blank=True, null=True)),
                ('rejection_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('withdraw_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('referral_rejected_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('rating', models.IntegerField(default=0)),
                ('acl', models.JSONField(default=dict)),
                ('assigned_lawyer_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.firmuser')),
                ('kind_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.legalmatterkind')),
                ('subscriber_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.subscriber')),
            ],
            options={
                'db_table': 'legalmatter',
            },
        ),
        migrations.AddField(
            model_name='document',
            name='legal_matter_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.legalmatter'),
        ),
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=50)),
                ('last_updated_timestamp', models.DateTimeField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('acl', models.JSONField(default=dict)),
                ('legal_matter_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.legalmatter')),
            ],
            options={
                'db_table': 'calendarevent',
            },
        ),
        migrations.CreateModel(
            name='LegalMatterIntakeData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('intake_form_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.intakeform')),
                ('legal_matter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.legalmatter')),
            ],
            options={
                'db_table': 'legalmatterintakedata',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('note', models.TextField()),
                ('created_timestamp', models.DateTimeField()),
                ('last_updated_timestamp', models.DateTimeField()),
                ('acl', models.JSONField(default=dict)),
                ('created_by_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes_created', to='my_app.firmuser')),
                ('legal_matter_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.legalmatter')),
                ('updated_by_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes_updated', to='my_app.firmuser')),
            ],
            options={
                'db_table': 'note',
            },
        ),
        migrations.CreateModel(
            name='CheckoutSession',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('expires_at', models.DateTimeField()),
                ('created', models.DateTimeField()),
                ('amount_subtotal', models.FloatField()),
                ('amount_total', models.FloatField()),
                ('url', models.URLField()),
                ('acl', models.JSONField(default=dict)),
                ('subscriber_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.subscriber')),
            ],
            options={
                'db_table': 'checkoutsession',
            },
        ),
        migrations.CreateModel(
            name='CalendarEventParticipant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('calendar_event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.calendarevent')),
                ('participant_firm_user_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.firmuser')),
                ('participant_subscriber_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.subscriber')),
            ],
            options={
                'db_table': 'calendareventparticipant',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_timestamp', models.DateTimeField()),
                ('last_updated_timestamp', models.DateTimeField()),
                ('completed_timestamp', models.DateTimeField(blank=True, null=True)),
                ('tracked_minutes', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=50)),
                ('assigned_timestamp', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('charge_type', models.CharField(blank=True, max_length=50, null=True)),
                ('charge_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('charge_amount', models.FloatField(default=0)),
                ('acl', models.JSONField(default=dict)),
                ('assigned_to_firm_user_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks_assigned', to='my_app.firmuser')),
                ('assigned_to_subscriber_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_app.subscriber')),
                ('created_by_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks_created', to='my_app.firmuser')),
                ('legal_matter_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.legalmatter')),
            ],
            options={
                'db_table': 'task',
            },
        ),
    ]
