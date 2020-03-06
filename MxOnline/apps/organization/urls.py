
from django.urls import path
from django.conf.urls import url
from django.views.generic import View

from apps.organization.views import OrgListView, AddAskView, DetailHomeView, DetailTeacherView, DetailCourseView, DetailDescView


urlpatterns = [
    url('^org_list/$', OrgListView.as_view(), name='org_list'),  # 课程机构列表页
    url('^add_ask/$', AddAskView.as_view(), name='add_ask'),  # 课程咨询
    url('^home/(?P<org_id>\d+)$', DetailHomeView.as_view(), name='home'),  # 课程机构首页
    url('^course/(?P<org_id>\d+)$', DetailCourseView.as_view(), name='course'),  # 课程机构课程页
    url('^teacher/(?P<org_id>\d+)$', DetailTeacherView.as_view(), name='teacher'),  # 课程机构讲师页
    url('^desc/(?P<org_id>\d+)$', DetailDescView.as_view(), name='desc'),  # 课程机构介绍页
]

