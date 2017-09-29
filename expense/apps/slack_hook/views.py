from rest_framework import viewsets, mixins, generics
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.mobile_api.models import UserProfile
from libs.slack_webhook import SlackWebHook


class DebtStatistic(APIView):
    """
    Register a new user OTP.
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        debt_statistic = []
        for user_profile in UserProfile.objects.all():
            if user_profile.account_balance < 0:
                debt_statistic.append([user_profile.name, user_profile.account_balance])
        SlackWebHook.send_debt_notifications(debt_statistic=debt_statistic)
        return Response({"text": "OK"})