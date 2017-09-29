# -*- coding: utf-8 -*-
import requests
from libs.utils import format_amount

expense_slack_hook = 'https://hooks.slack.com/services/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'
debt_slack_hook = 'https://hooks.slack.com/services/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'


class SlackWebHook(object):

    @classmethod
    def send_notifications(cls, text):
        data_send = {
            "link_names": 1,
            "text": text
        }
        requests.post(url=expense_slack_hook, json=data_send)

    @classmethod
    def send_debt_notifications(cls, debt_statistic):
        if not debt_statistic:
            return True
        debt_statistic = sorted(debt_statistic, key=lambda k: k[1])
        attachments = []
        data_send = {
          "link_names": 1,
          "attachments": attachments
        }

        for debt in debt_statistic:
            attachments.append({
              "color": "#FF0000",
              "text": u"<@%s> ơi, anh còn thiếu %s VND nè! Đóng luôn đi anh. Ahihi" %(debt[0],format_amount(abs(debt[1]))),
              "fields": []
            })
        requests.post(url=debt_slack_hook, json=data_send)
