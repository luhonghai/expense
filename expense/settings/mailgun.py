from .base import config

MAILGUN_API_BASE_URL = config.get("mailgun", "api_base_url")
MAILGUN_API_KEY = config.get("mailgun", "api_key")
MAILGUN_SENDER_EMAIL = config.get("mailgun", "sender_email")
ANYMAIL = {
    "MAILGUN_API_KEY": MAILGUN_API_KEY,
    "MAILGUN_API_URL": MAILGUN_API_BASE_URL,
    "MAILGUN_SENDER_DOMAIN": MAILGUN_SENDER_EMAIL
}

