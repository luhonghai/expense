import requests
slack_hook = 'https://hooks.slack.com/services/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'

class SlackWebHook(object):

    @classmethod
    def send_notifications(cls, text):
        data_send = {
            "username": "ExpenseBot",
            "text": text
        }
        requests.post(url=slack_hook, json=data_send)
