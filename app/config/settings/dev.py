from .base import *

DEV_JSON = json.load(open(os.path.join(SECRET_DIR, 'dev.json')))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')

WSGI_APPLICATION = 'config.wsgi.dev.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = DEV_JSON['DATABASES']
