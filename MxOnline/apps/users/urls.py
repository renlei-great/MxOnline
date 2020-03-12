
from django.urls import path
from django.conf.urls import url
from django.views.generic import View

from apps.users.views import LoginView, LogoutView, SendSmsView, MobileLoginView, RegisterView, UserInfoView, UploadImageView, UploadInfoView, UpdatePwdView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('send_sms/', SendSmsView.as_view(), name='dend_sms'),
    path('mobilelogin', MobileLoginView.as_view(), name='mobilelogin'),
    path('register/', RegisterView.as_view(), name='register'),

    url(r'^user_info$', UserInfoView.as_view(), name='user_info'),  # 个人中心-个人资料
    url(r'^upload_image$', UploadImageView.as_view(), name='upload_image'),  # 个人中心-个人资料-修改头像
    url(r'^upload_info$', UploadInfoView.as_view(), name='upload_info'),  # 个人中心-个人资料修改
    url(r'^update_pwd$', UpdatePwdView.as_view(), name='update_pwd'),  # 个人中心-个人资料修改

]
