
from django.conf.urls import url

from apps.courses.views import CourseListView, CourseDetailView, CourseLessonView, CourseCommentView, VideoView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='list'),  # 课程列表页显示
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='detail'),  # 课程详情页显示
    url(r'^lesson/(?P<course_id>\d+)$', CourseLessonView.as_view(), name='lesson'),  # 开始学习页显示
    url(r'^comment/(?P<course_id>\d+)$', CourseCommentView.as_view(), name='comment'),  # 开始学习评论页显示
    url(r'^play/(?P<course_id>\d+)/(?P<video_id>\d+)$', VideoView.as_view(), name='play'),  # 开始学习视屏页显示
]

