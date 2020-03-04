
from django.urls import path
from django.conf.urls import url
from django.views.generic import View

from apps.organization.views import OrgListView, AddAskView



urlpatterns = [
    url('^org_list/$', OrgListView.as_view(), name='org_list'),  # 课程机构列表页
    url('^add_ask/$', AddAskView.as_view(), name='add_ask'),  # 课程咨询
]
