from django.db import models
from django.conf import settings
from django.core.exceptions import FieldError
from django.utils.functional import cached_property

from .base import BaseModel


class UserGroup(BaseModel):
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.TextField()
    description = models.TextField()
    credit = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)

    def total_event(self, event_type=None):
        if event_type:
            return self.events.filter(event_type=event_type)
        else:
            return self.events.all()

    def collect_debt(self):
        for unpaid_transaction in self.unpaid_transactions():
            unpaid_transaction.paid_group_pending()

    @property
    def no_collection_event(self):
        from .event import Event
        return self.total_event(event_type=Event.TYPE_1).count()

    @property
    def no_paid_event(self):
        from .event import Event
        return self.total_event(event_type=Event.TYPE_2).count()

    def unpaid_transactions(self):
        from .transaction import Transaction
        return self.transactions.filter(
            is_user_paid=False,
            is_paid_for_group=False,
            group_id=self.id,
            user_id=None,
            status=Transaction.PENDING
        )
    @property
    def balance(self):
        unpaid_money = 0
        for unpaid_transaction in self.unpaid_transactions():
            unpaid_money += unpaid_transaction.amount
        return self.credit - unpaid_money

    @property
    def member_names(self):
        return ", ".join([user.userprofile.name for user in self.members.all()])
