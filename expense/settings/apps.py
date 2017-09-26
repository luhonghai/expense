INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize'
]


INSTALLED_APPS += [
    'django_extensions',
    'rest_framework',
    'rest_framework_jwt',
    'raven.contrib.django.raven_compat',
    'bootstrap3',
]


INSTALLED_APPS += [
    'apps.mobile_api',
    'apps.admin_v1',
    'django_crontab'
]
