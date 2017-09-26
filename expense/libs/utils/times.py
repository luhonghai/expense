from datetime import datetime, time
import pytz
from django.utils import timezone

SINGAPORE_TIMEZONE = 'Asia/Singapore'
DATE_FORMAT = "%b %-m %Y"
TIME_FORMAT = "%-H:%M"

def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.get_current_timezone())


def convert_datetime_to_utc(convert_time):
    if not isinstance(convert_time, datetime):
        raise ValueError("Convert time must be datetime instance")
    return convert_time.utcnow()


def pluralize_time(time_number, text="second"):
    if time_number > 1:
        text = "%ss" %text
    return "%s %s" %(time_number, text)


def display_time(seconds):
    result = []
    if seconds == 0:
        return "0 second"
    m, s = divmod(seconds, 60)
    if s > 0:
        result.append(pluralize_time(s))
    if m > 0:
        result.append(pluralize_time(m, text="minute"))
    h, m = divmod(m, 60)
    if h > 0:
        result.append(pluralize_time(h, text="hour"))
    result.reverse()
    return " ".join(result)


def convert_second_to_minute(seconds):
    return seconds/ 60.0


def convert_invoice_time_format(convert_time):
    tz = pytz.timezone(SINGAPORE_TIMEZONE)
    singapore_time = convert_time.astimezone(tz)
    return "on %s at %s" % (singapore_time.strftime(DATE_FORMAT), singapore_time.strftime(TIME_FORMAT))


def convert_timestamp_to_utc(timestamp):
    return datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)