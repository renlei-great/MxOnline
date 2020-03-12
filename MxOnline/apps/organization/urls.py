
from django.urls import path
from django.conf.urls import url
from django.views.generic import View

from apps.organization.views import OrgListView, AddAskView, DetailHomeView, DetailTeacherView, DetailCourseView, DetailDescView, TeacherListView, TeacherDetailView


urlpatterns = [
    url('^org_list/$', OrgListView.as_view(), name='org_list'),  # 课程机构列表页
    url('^add_ask/$', AddAskView.as_view(), name='add_ask'),  # 课程咨询
    url('^home/(?P<org_id>\d+)$', DetailHomeView.as_view(), name='home'),  # 课程机构首页
    url('^course/(?P<org_id>\d+)$', DetailCourseView.as_view(), name='course'),  # 课程机构课程页
    url('^teacher/(?P<org_id>\d+)$', DetailTeacherView.as_view(), name='teacher'),  # 课程机构讲师页
    url('^desc/(?P<org_id>\d+)$', DetailDescView.as_view(), name='desc'),  # 课程机构介绍页
    url(r'^teacher_list$', TeacherListView.as_view(), name='teacher_list'),  # 授课教师列表页显示
    url(r'^teacher_detail/(?P<teacher_id>\d+)$', TeacherDetailView.as_view(), name='teacher_detail'),  # 授课教师详情页显示
]

