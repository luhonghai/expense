import requests
from settings import MAILGUN_API_BASE_URL, MAILGUN_API_KEY, MAILGUN_SENDER_EMAIL


def send_email(subject, to_add, content, bcc=[], files=[]):
    """
    Used to send email
    *** Parameter ***
    - subject : string - subject of email.
    - from_add : string - sender address.
    - to_add : list - list of receiver address.
    """
    try:
        result = requests.post(
            MAILGUN_API_BASE_URL,
            auth=("api", MAILGUN_API_KEY),
            files=files,
            data={"from": MAILGUN_SENDER_EMAIL,
                  "to": to_add,
                  "bcc": bcc,
                  "subject": subject,
                  "text": "",
                  "html": content},
            verify=False)
    except Exception as e:
        return False, str(e)

    if result.status_code != 200:
        return False, result.text
    return True, result.text


def validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False