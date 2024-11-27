import os
import sys
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
    call_command('insert_subscriber', generate_ulid())
except Exception as e:
    print(f"Error running makemigrations: {e}")
