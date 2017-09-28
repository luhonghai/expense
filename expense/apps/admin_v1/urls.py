from django.conf.urls import url
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views
from .views import ProfileList
from .views import HomePageView
# from .views import SessionHistoryView, SessionActiveView, export_data, import_data, export_import_result, \
#     export_import_sample, configuration_view, SessionDetailView, CouponListView, CouponDetailView, \
#     SessionInstanceView, ProfileDetailView
from .views import ProfileDetailView, UserGroupDetailView, event_detail, paid_transaction

urlpatterns = [
    url(r'^home/$', HomePageView.as_view(), name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGIN_URL}, name='logout'),

    # Manage profile
    url(r'^profile/list/$', ProfileList.as_view(), name='profile_list'),
    url(r'^profile/detail/(?P<user_id>[\w-]+)$', ProfileDetailView.as_view(), name='profile_detail'),

    # Manage one user group
    url(r'^group/(?P<group_id>[\w-]+)$', UserGroupDetailView.as_view(), name='user_group_detail'),
    url(r'^group/(?P<group_id>[\w-]+)/event/$', event_detail, name='create_event'),
    url(r'^group/(?P<group_id>[\w-]+)/event/(?P<event_id>[\w-]+)$', event_detail, name='edit_event'),

    url(r'^transaction/(?P<transaction_id>[\w-]+)/$', paid_transaction, name='paid_transaction'),
]