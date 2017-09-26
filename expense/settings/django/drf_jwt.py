import os

from datetime import timedelta

from django.conf import settings

from ..base import CONFIG_FILE_DIR, config

PUBLIC_KEY_FILE = os.path.join(CONFIG_FILE_DIR, 'app.rsa.pub')
PRIVATE_KEY_FILE = os.path.join(CONFIG_FILE_DIR, 'app.rsa')

with open(PUBLIC_KEY_FILE) as fa, open(PRIVATE_KEY_FILE) as fb:
    PUBLIC_KEY = fa.read()
    # TODO: Remove private key
    PRIVATE_KEY = fb.read()


JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USERNAME_HANDLER':
    'rest_framework_jwt.utils.jwt_get_username_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': settings.SECRET_KEY,
    'JWT_PUBLIC_KEY': PUBLIC_KEY,
    'JWT_PRIVATE_KEY': PRIVATE_KEY,
    'JWT_ALGORITHM': 'RS256',
    'JWT_EXPIRATION_DELTA':timedelta(seconds=config.getint("jwt", "time_expiration")),
    'JWT_VERIFY_EXPIRATION': config.getboolean("jwt", "verify_expiration")
}
