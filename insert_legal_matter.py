import os
from tqdm import tqdm
import ulid
from django.core.management import call_command

# Ensure Django settings are configured
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rdbms.settings')
django.setup()

def generate_ulid():
    return str(ulid.ulid())

# Invoke `makemigrations`
try:
    subscriber_id = '01JD0BB5RN4J80W3795V430ZDS'
    group_id = '01JD0BD7BWYSTXJ45C7P8R578V'
    legal_matter_kind_id = '01JD0BEPAJHVNG5DB136KJDZQG'
    firm_id = '01JD0BBGJ25JZ7DRPFVFA1T6D9'
    call_command('insert_subscriber', subscriber_id)
    call_command('insert_firm', firm_id)
    call_command('insert_groups', group_id)
    call_command('insert_legal_matter_kind', legal_matter_kind_id)

    for i in tqdm(range(100)):
        lawyer_id = generate_ulid()

        call_command('insert_lawyers', lawyer_id, firm_id)
        call_command('insert_firm_user_group', lawyer_id, group_id)
        call_command('insert_legal_matter', subscriber_id, group_id, lawyer_id, legal_matter_kind_id)
except Exception as e:
    print(f"Error running makemigrations: {e}")
