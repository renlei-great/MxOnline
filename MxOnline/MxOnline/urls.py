"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import url
from django.views.static import serve

import apps.users.urls
import apps.organization.urls
import apps.operation.urls
import apps.courses.urls
from apps.users.views import IndexView
import xadmin
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('index/', IndexView.as_view(), name='index'),  # 主页
    path('users/', include((apps.users.urls, 'users'))),  # 用户模块
    path('org/', include((apps.organization.urls, 'org'))),  # 机构模块
    path('ope/', include((apps.operation.urls, 'ope'))),  # 用户相关操作模块
    path('course/', include((apps.courses.urls, 'course'))),  # 课程相关模块

    url(r'^captcha/', include('captcha.urls')),  # 验证码
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),  # 获取media文件
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),  # 获取static文件
    url(r'^ueditor/',include('DjangoUeditor.urls')),  # 富文本ｕｒｌ
]
