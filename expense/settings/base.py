import os
import configparser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6uapo=a$g9+8&iyzexsrwe+@(ofb&2b@tq4&^h6w^8zz$q5try'

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True

DEBUG = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django_crontab': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

STATIC_URL = '/static/'

# Add these new lines
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

LOGIN_REDIRECT_URL = "/admin_v1/profile/list/"
LOGIN_URL = "/admin_v1/login/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, "apps.conf"))
CONFIG_FILE_DIR = config.get("django", "config_file_path")
SALT_EMAIL_VALIDATE = config.get("django", "salt_email_validate")
EMAIL_VALIDATE_EXPIRATION = config.getint("django", "email_validate_expiration")
BASE_URL = config.get("django", "base_url")

FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")

EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"