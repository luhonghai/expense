from django.template import loader
# from django.core.mail import send_mail
from libs.utils import send_email
from settings import MAILGUN_SENDER_EMAIL
from django.core.mail import EmailMultiAlternatives
from django.template import Context

class LottoMailServices(object):

    @classmethod
    def send_email(cls, subject, to_add, content, html_content):

        # msg = EmailMultiAlternatives(subject=subject, from_email=MAILGUN_SENDER_EMAIL,
        #                              to=[to_add], body=content)
        # msg.attach_alternative(html_content, "text/html")
        # return msg.send()
        return send_email(subject=subject, to_add=to_add, content=html_content)

    @classmethod
    def send_verify_email(cls, recipient, verify_link):
        subject = "Verify Email"
        text_body = "Verify Email"
        context_data = {
            "verify_link": verify_link
        }
        html_body = loader.render_to_string('email/verify_email.html', context=context_data)
        return cls.send_email(subject=subject, to_add=recipient, content=text_body, html_content=html_body)

    @classmethod
    def send_forgot_pin(cls, recipient, forgot_token):
        subject = "Forgot pin"
        text_body = "Forgot pin"
        context_data = {
            "forgot_token": forgot_token
        }
        html_body = loader.render_to_string('email/forgot_pin.html', context=context_data)
        return cls.send_email(subject=subject, to_add=recipient, content=text_body, html_content=html_body)

    @classmethod
    def send_winning_prize(cls, recipient, prize, prize_value):
        subject = "Test You are winner"
        text_body = "You are winner"
        context_data = {
            "prize": prize,
            "prize_value": prize_value,
        }
        html_body = loader.render_to_string('email/winning_prize.html', context=context_data)
        return cls.send_email(subject=subject, to_add=recipient, content=text_body, html_content=html_body)