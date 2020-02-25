
from django.urls import path
from django.views.generic import View

from apps.users.views import LoginView



urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
