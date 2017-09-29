from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from apps.mobile_api.models import UserGroup, UserProfile
from apps.admin_v1.constant import *

class Command(BaseCommand):

    def update_user_id(self, name, slack_id):
        try:
            user_profile = UserProfile.objects.get(name=name)
            user_profile.slack_id = slack_id
            user_profile.save()
            print "%s updated" % (name)
        except Exception, e:
            print "%s not found" % (name)



    def handle(self, *args, **options):
        user_slack_ids = [
            ["U76NZKBEJ", "number.1"],
            ["U75B0NK1P", "number.2"],
            ["U760W6C77", "number.3"],
            ["U76UVP1NK", "number.4"],
            ["U76NY1SKG", "number.6"],
            ["U75B8GPR7", "number.7"],
            ["U760XL6RK", "number.8"],
            ["U75Q1CH6F", "number.9"],
            ["U76V26ZST", "number.11"],
            ["U75UDSQAE", "number.12"],
            ["U76NYS0GN", "number.22"],
         ]
        for slack_id in user_slack_ids:
            self.update_user_id(name=slack_id[1], slack_id=slack_id[0])






