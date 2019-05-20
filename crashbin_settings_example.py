# Copy this file to crashbin_settings.py to configure crashbin settings.

import pathlib

HOMEDIR = pathlib.Path.home() / '.crashbin'

DATABASE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': HOMEDIR / 'db.sqlite3',
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Zurich'
MEDIA_ROOT = HOMEDIR / 'media'

EMAIL = {
    'backend': 'console',

    'smtp_host': None,
    'smtp_port': None,
    'smtp_user': None,
    'smtp_password': None,
    'smtp_tls': None,

    'incoming_url': None,
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3^p5wti7slr#md+2)4xl(w$bmce3-==&0awxws7w(y_=^2izxm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CUSTOM_CSS = """
"""
