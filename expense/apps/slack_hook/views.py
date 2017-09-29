# -*- coding: utf-8 -*-
from libs.utils import format_amount
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


NO_DEBT = u"Anh ah, không ai nợ. Anh yên đi nhé! :blush:"
HAS_DEBT = u"Anh ah, có %s bác đang nợ. Em báo lên group anh nhé! :blush:"
NOT_FOUND_USER = u"Anh ơi, em không tìm anh này. Anh check lại giúp em với! :blush:"
NOT_DEBT_USER = u"Anh ơi, anh không nợ gì cả đâu ạ. Hiện tại anh còn %s VND! :blush:"
DEBT_USER = u"Anh đang còn nợ %s VND. Anh trả tiền ngay nhé :blush:"

class DebtStatistic(APIView):
    """
    Register a new user OTP.
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        debt_statistic = []
        response_text = ""
        detail = request.GET("text")
        if not detail:
            for user_profile in UserProfile.objects.all():
                if user_profile.account_balance < 0:
                    debt_statistic.append([user_profile.slack_id, user_profile.account_balance])
            if debt_statistic:
                SlackWebHook.send_debt_notifications(debt_statistic=debt_statistic)
                response_text = HAS_DEBT % len(debt_statistic)
            else:
                response_text = NO_DEBT
        else:
            try:
                user_profile = UserProfile.objects.get(name=detail)
            except Exception:
                response_text = NOT_FOUND_USER
            if user_profile.unpaid_transactions.count() == 0:
                response_text = NOT_DEBT_USER % format_amount(abs(user_profile.account_balance))
            else:
                response_text = DEBT_USER % format_amount(abs(user_profile.account_balance))

        data_send = {"text": response_text, "link_names": 1}
        return Response(data_send)