from django import template
from ..constant import *
from urlparse import urlparse
register = template.Library()


@register.filter(name='format_page_url')
def format_page_url(value, page):
    url_params = {}
    try:
        list_url_params = value.split("&")
        for param in list_url_params:
            key, value = param.split("=")
            if key == "page":
                continue
            if not value:
                continue
            url_params[key]=value
    except Exception:
        pass
    url_params["page"]=page
    return urlparse.urlencode(url_params)


@register.filter(name='format_transaction_status')
def format_transaction_status(value):
    if value:
        return "Completed"
    else:
        return "Pending"

@register.filter(name='format_event_type')
def format_transaction_status(value):
    from apps.mobile_api.models import Event
    for event in Event.EVENT_TYPES:
        if value == event[0]:
            return event[1]

@register.filter(name='format_event_status')
def format_transaction_status(value):
    if value:
        return "Completed"
    else:
        return "Chua hoan thanh"

@register.filter(name='format_payer')
def format_transaction_status(value):
    if value.user:
        return value.user.userprofile.name
    return value.group.name

@register.filter(name='show_source_money')
def show_source_money(value):
    from apps.mobile_api.models import Event
    if value.event_type == Event.TYPE_1:
        source = Event.SOURCE_INDIVIDUAL
    else:
        source = value.source_money
    for source_type in Event.SOURCE_TYPES:
        if source == source_type[0]:
            return source_type[1]
