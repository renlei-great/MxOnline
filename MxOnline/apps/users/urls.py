
from django.urls import path
from django.views.generic import View

from apps.users.views import LoginView, LogoutView, SendSmsView



urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('send_sms/', SendSmsView.as_view(), name='dend_sms')
]
