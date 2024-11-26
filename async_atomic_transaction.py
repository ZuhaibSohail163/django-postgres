import os
import sys
from django.core.management import call_command

# Ensure Django settings are configured
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rdbms.settings')
django.setup()

try:
    call_command('async_atomic_transaction')
except Exception as e:
    print(f"Error running makemigrations: {e}")
