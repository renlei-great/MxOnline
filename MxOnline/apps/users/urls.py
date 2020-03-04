
from django.urls import path
from django.views.generic import View

from apps.users.views import LoginView, LogoutView, SendSmsView, MobileLoginView, RegisterView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('send_sms/', SendSmsView.as_view(), name='dend_sms'),
    path('mobilelogin', MobileLoginView.as_view(), name='mobilelogin'),
    path('register/', RegisterView.as_view(), name='register')
]
