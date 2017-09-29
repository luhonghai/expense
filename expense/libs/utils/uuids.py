import uuid
from random import choice
from string import ascii_lowercase, digits

def generate_uuid():
    return str(uuid.uuid4())


def generate_random_text(length=16, chars=ascii_lowercase+digits, split=4, delimiter='-'):

    username = ''.join([choice(chars) for i in range(length)])

    if split:
        username = delimiter.join([username[start:start+split] for start in range(0, len(username), split)])

    return username

import locale

def format_amount(amount):
    locale.setlocale(locale.LC_ALL, '')
    locale._override_localeconv = {'mon_thousands_sep': '.'}
    return locale.format('%f', int(amount), grouping=True, monetary=True)