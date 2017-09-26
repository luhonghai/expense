from django.conf.urls import url, include
from django.contrib import admin

from apps.admin_v1 import urls as admin_v1_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin_v1/', include(admin_v1_urls, namespace='admin_v1'))
]
