# -*- coding: utf-8 -*-
from django.db import models
from libs.mail_services import LottoMailServices
from .base import BaseModel
from libs.utils import generate_otp, format_amount
from .user_profile import UserProfile
from django.utils import timezone
from django.conf import settings
from libs.slack_webhook import SlackWebHook


class Transaction(BaseModel):
    PLUS, MINUS = xrange(2)
    PENDING, COMPLETED = xrange(2)
    from .user_group import UserGroup
    from .event import Event
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
        null=True
    )
    group = models.ForeignKey(
        UserGroup,
        on_delete=models.CASCADE,
        related_name="transactions",
        null=True
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="transactions",
        null=True
    )
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    type = models.IntegerField(default=PLUS)
    description = models.TextField(default="")
    status = models.IntegerField(default=PENDING)
    is_user_paid = models.BooleanField(default=True)
    paid_at = models.DateTimeField(null=True)
    is_paid_for_group = models.BooleanField(default=False)

    def paid_user_pending(self, is_adding=True):
        if self.status != self.PENDING:
            return False
        if not self.user:
            return False
        if is_adding:
            Transaction.create_add_transaction(
                user=self.user,
                amount=self.amount,
                group_id=None if not self.group else self.group_id,
                event_id=None if not self.event else self.event_id
            )
        if self.user.userprofile.credit >= self.amount:
            self.user.userprofile.credit -= self.amount
            self.user.userprofile.save()
            self.status = self.COMPLETED
            self.paid_at = timezone.now()
            self.save()
            if self.is_paid_for_group:
                self.group.credit += self.amount
                self.group.save()
                self.group.collect_debt()
            SlackWebHook.send_notifications(
                text=u"%s : %s VND" %(self.description, format_amount(self.amount))
            )

    @classmethod
    def create_add_transaction(cls, user, amount, description=None, **kwargs):
        if not description:
            description = u"Nạp tiền vào tài khoản"
        added_transaction = cls.objects.create(
            user=user,
            amount=amount,
            type=cls.PLUS,
            description=description,
            paid_at=timezone.now(),
            status=cls.COMPLETED
        )
        user.userprofile.credit += amount
        user.userprofile.save()
        if kwargs.has_key("group_id"):
            added_transaction.group_id = kwargs.get("group_id")
        if kwargs.has_key("event_id"):
            added_transaction.event_id = kwargs.get("event_id")
        added_transaction.save()
        try:
            SlackWebHook.send_notifications(
                text=u"<@%s> nạp %s VND vào tài khoản" %(user.userprofile.slack_id, format_amount(amount))
            )
        except Exception:
            pass
        return added_transaction

    @classmethod
    def create_user_paid_transaction(cls, user, amount, description, group, paid_group=True, **kwargs):
        paid_transaction = cls.objects.create(
            user=user,
            amount=amount,
            type=cls.MINUS,
            description=description,
            group=group
        )
        if paid_group:
            paid_transaction.is_paid_for_group = True
        if user.userprofile.credit >= amount:
            user.userprofile.credit -= amount
            user.userprofile.save()
            paid_transaction.status = cls.COMPLETED
            paid_transaction.paid_at = timezone.now()
            if paid_group:
                group.credit += amount
                group.save()
            try:
                SlackWebHook.send_notifications(
                    text="%s : %s VND" %(description, amount)
                )
            except Exception:
                pass
        if kwargs.has_key("event_id"):
            paid_transaction.event_id = kwargs.get("event_id")
        paid_transaction.save()

    @classmethod
    def create_group_paid_transaction(cls, amount, description, group, event):
        paid_transaction = cls.objects.create(
            amount=amount,
            type=cls.MINUS,
            description=description,
            group=group,
            is_user_paid=False,
            event=event
        )
        if group.credit >= amount:
            group.credit -= amount
            group.save()
            paid_transaction.status = cls.COMPLETED
            paid_transaction.paid_at = timezone.now()
            try:
                SlackWebHook.send_notifications(
                    text="%s : %s VND" %(description, amount)
                )
            except Exception:
                pass
        paid_transaction.save()

    def paid_group_pending(self):
        if self.status != self.PENDING:
            return False
        if self.user:
            return False
        if self.group.credit < self.amount:
            return False
        self.group.credit -= self.amount
        self.group.save()
        self.status = self.COMPLETED
        self.paid_at = timezone.now()
        try:
            SlackWebHook.send_notifications(
                text="%s : %s VND" %(self.description, self.amount)
            )
        except Exception:
            pass
        self.save()




