# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from .base import BaseModel
from .user_group import UserGroup


class Event(BaseModel):
    TYPE_1, TYPE_2 = xrange(2)
    SOURCE_GROUP, SOURCE_INDIVIDUAL = xrange(2)

    EVENT_TYPES = (
        (TYPE_1, 'Collecting'),
        (TYPE_2, 'Spent')
    )

    SOURCE_TYPES =(
        (SOURCE_GROUP, 'Group'),
        (SOURCE_INDIVIDUAL, 'Individual')
    )

    group = models.ForeignKey(
        UserGroup,
        on_delete=models.CASCADE,
        related_name="events"
    )
    event_type = models.SmallIntegerField(
        choices=EVENT_TYPES)

    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    description = models.TextField(default=None)
    source_money = models.SmallIntegerField(choices=SOURCE_TYPES, default=SOURCE_GROUP)
    member_join = models.TextField(null=True)

    def collecting_money(self):
        from .transaction import Transaction
        if self.event_type == self.TYPE_1:
            for user in self.group.members.filter(id__in=self.member_join_list):
                Transaction.create_user_paid_transaction(
                    user=user,
                    amount=self.amount,
                    description=u"@%s đóng tiền vào quỹ '%s' cho event '%s'" %(user.userprofile.name, self.group.name, self.description),
                    group=self.group,
                    paid_group=True,
                    event_id=self.id
                )
        if self.event_type == self.TYPE_2:
            if self.source_money == self.SOURCE_GROUP:
                Transaction.create_group_paid_transaction(
                    amount=self.amount,
                    description=u"%s trả tiền cho event '%s'" %(self.group.name, self.description),
                    group=self.group,
                    event=self
                )
            if self.source_money == self.SOURCE_INDIVIDUAL:
                for user in self.group.members.filter(id__in=self.member_join_list):
                    Transaction.create_user_paid_transaction(
                        user=user,
                        amount=self.amount,
                        description=u"@%s trả tiền cho event '%s' của '%s'" %(user.userprofile.name, self.description, self.group.name),
                        group=self.group,
                        paid_group=False,
                        event_id=self.id
                    )

    @property
    def event_complete_status(self):
        from .transaction import Transaction
        if self.transactions.filter(status=Transaction.PENDING).count() > 0:
            return False
        return True

    @property
    def member_join_list(self):
        return [int(member) for member in self.member_join.split(",")]