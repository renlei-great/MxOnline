from django.conf.urls import url

from apps.operation.views import OpeColView


urlpatterns = [
    # url('^org_list/$', OrgListView.as_view(), name='org_list'),  # 课程机构列表页
    url('^col/$', OpeColView.as_view(), name='col'),  # 机构收藏处理
]

