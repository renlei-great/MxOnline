
from django.urls import path
from django.conf.urls import url
from django.views.generic import View

from apps.organization.views import OrgListView



urlpatterns = [
    url('^org_list/(?P<age>\d+)$', OrgListView.as_view(), name='org_list')
]
