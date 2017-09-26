from django import template
from ..constant import *
from django.conf import settings
from pytz import timezone

register = template.Library()


@register.filter(name='display_local')
def display_local(value):
    if not value:
        return ""
    return value.astimezone(tz=timezone(settings.TIME_ZONE)).strftime(DISPLAY_TIME_FORMAT)