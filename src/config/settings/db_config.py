import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGSQL_DB_NAME', ''),
        'USER': os.getenv('PGSQL_USER', ''),
        'PASSWORD': os.getenv('PGSQL_PASSWORD', ''),
        'HOST': os.getenv('PGSQL_HOST', ''),
        'PORT': os.getenv('PGSQL_PORT', ''),
    }
}