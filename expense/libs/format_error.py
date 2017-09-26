# -*- coding: utf-8 -*-
import collections
import re

from rest_framework.views import exception_handler as default_django_rest_exception  # NOQA
from raven.contrib.django.raven_compat.models import sentry_exception_handler
from rest_framework.response import Response


ERROR_DATA_FORMAT = {
    'code': 400,
    'message': "",
    'errors': {}
}

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).iteritems())
        else:
            items.append((new_key, v))
    return dict(items)


def replace_dot_without_decimal(msg):
    p = re.compile("(?<=\d)(\.)(?!\d)")
    return p.sub("", msg)


def sanitize_message(msg):
    if isinstance(msg, list):
        msg = u'. '.join(replace_dot_without_decimal(v) for v in msg)
    else:
        msg = msg.replace('.', '')
    return msg


def get_message_from_errors(errors):
    if isinstance(errors, dict):
        errors = flatten(errors)
        errors = errors.values()
    return u'. '.join(sanitize_message(v) for v in errors)


def get_error_data(status_code, errors):
    message = get_message_from_errors(errors)
    error_data = ERROR_DATA_FORMAT
    error_data["code"] = status_code
    error_data["message"] = message
    error_data["errors"] = status_code

    return error_data

def exception_handler(exc, context):
    response = default_django_rest_exception(exc, context)
    if response is None:
        return response

    data = get_error_data(response.status_code, response.data)
    response.data = data
    return response
