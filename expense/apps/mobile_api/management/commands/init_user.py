from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from apps.mobile_api.models import UserProfile
from apps.admin_v1.constant import *

class Command(BaseCommand):

    def create_user(self, phone_number, name):
        User = get_user_model()
        try:
            user = User.objects.create_user(username=phone_number, password=phone_number)
            user_profile, _ = UserProfile.objects.get_or_create(
                user=user,
                phone_number=phone_number,
                name=name
            )
            print "Created %s - %s" % (name, phone_number)
        except Exception, e:
            print "%s - %s already created" % (name, phone_number)


    def handle(self, *args, **options):
        user_list = [
            ["0988258252", "number.1"],
            ["0978721168", "number.2"],
            ["0986899787", "number.3"],
            ["01695354095", "number.4"],
            ["01656113334", "number.6"],
            ["0979203108", "number.7"],
            ["0986090323", "number.8"],
            ["0963245626", "number.9"],
            ["0904505201", "number.11"],
            ["01649819299", "number.12"],
            ["01244881992", "number.22"],
        ]
        for user in user_list:
            self.create_user(phone_number=user[0], name=user[1])






