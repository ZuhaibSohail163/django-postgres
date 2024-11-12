import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
sys.path.append(BASE_DIR)  # Add the project root to the Python path
DEBUG = True

INSTALLED_APPS = [
    "django.contrib.postgres",
    "legal_fix",
]



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_legal_fix',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
