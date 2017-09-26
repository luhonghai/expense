# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
from .base import BASE_DIR
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
