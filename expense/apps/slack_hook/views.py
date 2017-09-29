from rest_framework import viewsets, mixins, generics
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework import status
from rest_framework.permissions import AllowAny


class DebtStatistic(APIView):
    """
    Register a new user OTP.
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):

        return Response({
            "username": "ExpenseBot",
            "text": "abc"
        })