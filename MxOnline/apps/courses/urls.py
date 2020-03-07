
from django.conf.urls import url

from apps.courses.views import CourseListView, CourseDetailView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='list'),  # 课程列表页显示
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='detail'),  # 课程详情页显示
]

