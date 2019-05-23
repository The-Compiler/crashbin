# Copy this file to crashbin_settings.py to configure crashbin settings.

import typing
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
    # Regex for incoming messages. The capture group needs to capture the
    # report ID.
    'incoming_subject': r'.*qutebrowser report #(.*)',

    'outgoing_subject': 'qutebrowser report #{}',
    'outgoing_address': 'crashbin@qutebrowser.org',
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3^p5wti7slr#md+2)4xl(w$bmce3-==&0awxws7w(y_=^2izxm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []  # type: typing.List[str]

CUSTOM_CSS = """
"""

# Name of the bin to be used as an inbox.
INBOX_BIN = "Inbox"

# Suggested colors for labels
LABEL_COLORS = ['#0033CC', '#428BCA', '#44AD8E', '#A8D695', '#5CB85C',
                '#69D100', '#004E00', '#34495E', '#7F8C8D', '#A295D6',
                '#5843AD', '#8E44AD', '#FFECDB', '#AD4363', '#D10069',
                '#CC0033', '#FF0000', '#D9534F', '#D1D100', '#F0AD4E',
                '#AD8D43']
