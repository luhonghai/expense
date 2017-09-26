# -*- coding: utf-8 -*-
from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from rest_framework import status


class PasswordError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Password must be 4 character')


class EmailAlreadyValidatedError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Email already validated.')


class EmailNotFoundError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Email not found')


class CouponCodeNotAvailableError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('This coupon not available.')

