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
HAS_DEBT = u"Anh ah, có %s bác đang nợ. Em báo lên group rồi anh nhé! :blush:"
NOT_FOUND_USER = u"Anh ơi, em không tìm anh này. Anh check lại giúp em với! :blush:"
NOT_DEBT_USER = u"Anh ơi, anh không nợ gì cả đâu ạ. Hiện tại anh còn %s VND! :blush:"
NOT_DEBT_OTHER_USER = u"Anh <@%s> không nợ gì cả đâu ạ. Hiện tại anh ấy còn %s VND! :blush:"
DEBT_USER = u"Anh đang còn nợ %s VND. Anh trả tiền ngay nhé :blush:"
DEBT_OTHER_USER = u"Anh <@%s> đang còn nợ %s VND. Anh nhắc anh ấy giúp em nhé :blush:"
NUMBER_HISTORY_INVALID = u"Anh <@%s> ơi, anh vui lòng điền số sau history giúp em với nhé. :blush:"


class DebtStatistic(APIView):
    """
    Register a new user OTP.
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        debt_statistic = []
        detail = request.GET.get("text")
        request_user = request.GET.get("user_id")
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
            if "history" in detail:
                try:
                    num_of_history = int(detail.split(" ")[1].strip())
                    user_profile = UserProfile.objects.get(slack_id=request_user)
                    all_transactions = user_profile.all_transactions(limit=num_of_history)
                    data_send = SlackWebHook.generate_history_notifications(transactions=all_transactions)
                    return Response(data_send)
                except Exception:
                    response_text = NUMBER_HISTORY_INVALID %request_user

            else:
                try:
                    user_profile = UserProfile.objects.get(name=detail)
                    if user_profile.unpaid_transactions().count() == 0:
                        if user_profile.slack_id == request_user:
                            response_text = NOT_DEBT_USER % format_amount(abs(user_profile.account_balance))
                        else:
                            response_text = NOT_DEBT_OTHER_USER % (user_profile.slack_id, format_amount(abs(user_profile.account_balance)))
                    else:
                        if user_profile.slack_id == request_user:
                            response_text = DEBT_USER % format_amount(abs(user_profile.account_balance))
                        else:
                            response_text = DEBT_OTHER_USER % (user_profile.slack_id, format_amount(abs(user_profile.account_balance)))
                except Exception:
                    response_text = NOT_FOUND_USER

        data_send = {"text": response_text, "link_names": 1}
        return Response(data_send)