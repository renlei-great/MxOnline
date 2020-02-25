from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth import authenticate, login
# from django.http.response import HttpResponseRedirect
# from django.urls import reverse
from apps.users.forms import LoginForm


# Create your views here.

# /users/login
class LoginView(View):
    """登录页面"""

    def get(self, request):
        """登录页面显示"""
        return render(request, 'login.html')

    def post(self, request):
        # 接受数据
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")

        # 校验数据
        # if not all([username, password]):
        #     return render(request, 'login.html', {'errage':'数据不完整'})
        login_form = LoginForm(request.POST)
        # 判断是够通过表单验证
        if login_form.is_valid():
            # 取出表单清洗的数据
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # 判断用户名和密码是否正确
            user = authenticate(username=username, password=password)
            if user is not None:  # 用户名密码正确
                # 记住用户登录状态
                login(request, user)

                # 返回首页
                return redirect(reverse('index'))

            else:  # 密码不正确
                return render(request, 'login.html', {'errage': '用户名或密码不正确', 'login_form': login_form})
        else:
            # 返回数据
            return render(request, 'login.html', {'login_form': login_form})
