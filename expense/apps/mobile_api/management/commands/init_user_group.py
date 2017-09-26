from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from apps.mobile_api.models import UserGroup, UserProfile
from apps.admin_v1.constant import *

class Command(BaseCommand):

    def create_user_group(self, name, users):
        try:
            user_group, _ = UserGroup.objects.get_or_create(
                name=name,
                description=name
            )
            print "Created %s" % (name)
        except Exception, e:
            user_group = UserGroup.objects.get(name=name)
            print "%s already created" % (name)
        for user in users:
            try:
                user_profile = UserProfile.objects.get(phone_number=user[0])
                user_group.members.add(user_profile.user)
                print "Added user - %s" % (user[0])
            except Exception, e:
                print str(e)


    def handle(self, *args, **options):
        user_groups = [
            ["Tobeyoungagain Group",
             [
                ["0988258252", "Number.1"],
                ["0978721168", "Number.2"],
                ["0986899787", "Number.3"],
                ["01695354095", "Number.4"],
                ["01656113334", "Number.6"],
                ["0979203108", "Number.7"],
                ["0986090323", "Number.8"],
                ["0963245626", "Number.9"],
                ["0904505201", "Number.11"],
                ["01649819299", "Number.12"],
                ["01244881992", "Number.22"],
             ]],
            ["Sport Club", [
                ["0988258252", "Number.1"],
                ["0978721168", "Number.2"],
                ["0986899787", "Number.3"],
                ["01695354095", "Number.4"],
                ["0986090323", "Number.8"],
                ["0963245626", "Number.9"],
                ["01244881992", "Number.22"],
            ]],
            ["TrungVitLon Club", [
                ["0988258252", "Number.1"],
                ["0978721168", "Number.2"],
                ["0986899787", "Number.3"],
                ["01695354095", "Number.4"],
                ["01656113334", "Number.6"],
                ["0979203108", "Number.7"],
                ["0986090323", "Number.8"],
                ["0963245626", "Number.9"],
                ["0904505201", "Number.11"],
                ["01649819299", "Number.12"],
                ["01244881992", "Number.22"],
            ]]
        ]
        for user_group in user_groups:
            self.create_user_group(name=user_group[0], users=user_group[1])






