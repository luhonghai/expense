from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core import signing
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property

from .base import BaseUserModel
from libs.utils import generate_random_text
from libs.utils import send_email, generate_otp
from libs.mail_services import LottoMailServices
from settings import SALT_EMAIL_VALIDATE, BASE_URL



class UserProfile(BaseUserModel):
    DEFAULT_PASSWORD = "123456"

    phone_number = models.CharField(default="", max_length=255, unique=True)
    email = models.EmailField(default="")
    name = models.CharField(default="", max_length=255)
    credit = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)

    def unpaid_transactions(self):
        from .transaction import Transaction
        return self.user.transactions.filter(
            is_user_paid=True,
            user_id=self.user_id,
            status=Transaction.PENDING
        )

    @property
    def account_balance(self):
        unpaid_money = 0
        for unpaid_transaction in self.unpaid_transactions():
            unpaid_money += unpaid_transaction.amount
        return self.credit - unpaid_money

    def recharge_money(self, amount):
        from .transaction import Transaction
        Transaction.create_add_transaction(user=self.user, amount=amount)
        for unpaid_transaction in self.unpaid_transactions().order_by("amount"):
            unpaid_transaction.paid_user_pending(is_adding=False)