from django.conf.urls import url
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    url(r'^debt_statistic/$', DebtStatistic.as_view(), name='debt_statistic'),

]