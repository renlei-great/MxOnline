from django.urls import path
from django.conf.urls import url
from django.views.generic import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from apps.users.views import LoginView, LogoutView, SendSmsView, MobileLoginView, RegisterView, UserInfoView, \
    UploadImageView, UploadInfoView, UpdatePwdView
from apps.users.views import UpdateMobileView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, UsersMessageView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('send_sms/', SendSmsView.as_view(), name='dend_sms'),
    path('mobilelogin', MobileLoginView.as_view(), name='mobilelogin'),
    path('register/', RegisterView.as_view(), name='register'),

    # 个人中心
    url(r'^user_info$', UserInfoView.as_view(), name='user_info'),  # 个人中心-个人资料
    url(r'^upload_image$', UploadImageView.as_view(), name='upload_image'),  # 个人中心-个人资料-修改头像
    url(r'^upload_info$', UploadInfoView.as_view(), name='upload_info'),  # 个人中心-个人资料修改
    url(r'^update_pwd$', UpdatePwdView.as_view(), name='update_pwd'),  # 个人中心-个人资料密码修改
    url(r'^update_mobile$', UpdateMobileView.as_view(), name='update_mobile'),  # 个人中心-个人资料手机号修改

    # 我的课程
    url(r'^mycourse$', login_required(TemplateView.as_view(template_name='usercenter-mycourse.html')), kwargs={'active': 'mycourse'}, name='mycourse'),

    # 我的收藏
    url(r'^fav_org$', MyFavOrgView.as_view(), name='fav_org'),  # 我的收藏-课程机构
    url(r'^fav_teacher$', MyFavTeacherView.as_view(), name='fav_teacher'),  # 我的收藏-授课教师
    url(r'^fav_course$', MyFavCourseView.as_view(), name='fav_course'),  # 我的收藏-收藏的课程

    # 我的消息
    url(r'^message$', UsersMessageView.as_view(), name='massage'),  # 个人中心-消息页面


]
