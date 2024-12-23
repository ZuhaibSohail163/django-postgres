import os
import sys
from django.core.management import call_command

# Ensure Django settings are configured
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rdbms.settings')
django.setup()

# Invoke `makemigrations`
try:
    call_command('makemigrations', 'django_rdbms')
except Exception as e:
    print(f"Error running makemigrations: {e}")
