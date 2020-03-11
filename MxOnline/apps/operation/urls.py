from django.conf.urls import url

from apps.operation.views import OpeColView, OpeCommentView


urlpatterns = [
    url('^col/$', OpeColView.as_view(), name='col'),  # 机构收藏处理
    url('^comment/$', OpeCommentView.as_view(), name='comment'),  # 提交评论处理
]

