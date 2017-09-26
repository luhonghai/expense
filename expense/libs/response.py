# -*- coding: utf-8 -*-
from rest_framework.response import Response

from rest_framework import status


class ActionSuccessResponse(Response):

    def __init__(self, data={}):
        super(ActionSuccessResponse, self).__init__()
        self.data = {"status": "success"}
        self.data.update(data)
