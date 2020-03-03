from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect, JsonResponse
# from django.urls import reverse
import redis

from apps.users.forms import LoginForm, CaptchaForm, MobileLoginForm, RegisterForm, RegisterPostForm
from MxOnline.settings import APIKEY
from utils import RandomStr, YunPian
from apps.users.models import UserProfile


# /users/register
class RegisterView(View):
    """注册页面"""
    def get(self, request):
        """显示页面"""
        register_captcha = RegisterForm(request.POST)
        return render(request, 'register.html', {'register_captcha': register_captcha})

    def post(self, request):
        """注册提交"""
        # 校验数据
        register_captcha = RegisterForm(request.POST)
        register_post = RegisterPostForm(request.POST)

        # 取出一个错误
        error_val = ''
        error_key = ''
        for key, val in register_post.errors.items():
            error_val = val[0]
            error_key = key
            break

        if not register_post.is_valid():
            return render(request, 'register.html', {
                'register_captcha': register_captcha,
                'register_post': register_post,
                'error_val': error_val,
                'error_key': error_key,
            })

        # 业务逻辑处理：注册用户
        mobile = register_post.cleaned_data['mobile']
        password = register_post.cleaned_data['password']
        # 注册用户
        user = UserProfile()
        user.username = mobile
        user.mobile = mobile
        user.set_password(password)
        user.save()

        # 验证通过，返回到登录页面
        return redirect(reverse('users:login'))


# /users/mobilelogin
class MobileLoginView(View):
    def post(self, request):
        # 校验数据
        mobile_login_form = MobileLoginForm(request.POST)
        if not mobile_login_form.is_valid():
            # 校验数据不对
            # 生成验证码
            d_mobile_form = CaptchaForm(request.POST)
            return render(request, 'login.html', {'mobile_login_form': mobile_login_form,
                                                  'd_mobile_form': d_mobile_form,
                                                  'res': 2})

        # 接收数据
        mobile = mobile_login_form.cleaned_data['mobile']
        code = mobile_login_form.cleaned_data['code']

        # 查询是否有此用户
        try:
            user = UserProfile.objects.get(mobile=mobile)
        except UserProfile.DoesNotExist:
            user = UserProfile()
            user.username = mobile
            user.mobile = mobile
            user.set_password(RandomStr.random_str(8, 2))
            user.save()

        # 记住用户登录状态
        login(request, user)

        # 返回数据：进入首页
        return redirect(reverse('index'))


# /users/send_sms/
class SendSmsView(View):
    """发送手机验证码"""
    def post(self, request):
        # 校验数据
        login_send_form = CaptchaForm(request.POST)
        redis.Redis()

        # 验证数据是否通过，处理核心逻辑
        res_dict = {}
        if login_send_form.is_valid():
            # 验证通过
            # 组织数据
            mobile = login_send_form.cleaned_data['mobile']
            apikey = APIKEY
            andom = RandomStr.random_str(4, 1)

            # 发送短信
            res_send = YunPian.send_captcha(apikey, mobile, andom)

            # 校验发送短信返回结果
            if res_send['code'] is 0:
                # 发送成功
                # 链接redis数据库
                rds = redis.Redis()
                # 设置电话号和验证吗
                rds.set(mobile, andom)
                # 设置键的过期时间
                rds.expire(mobile, 60*5)

                # 组织返回的数据
                res_dict['status'] = 'success'
            else:
                # 发送失败
                msg = res_send['msg']
                res_dict['msg'] = msg
        else:
            # 验证未通过
            for key, value in login_send_form.errors.items():
                res_dict[key] = value[0]

        # 返回
        return JsonResponse(res_dict)


# /users/login
class LoginView(View):
    """登录"""
    def get(self, request):
        """登录页面显示"""
        user = request.user
        if user.is_authenticated:   # is_authenticated
            return redirect(reverse('index'))
        login_form = CaptchaForm(request.POST)

        return render(request, 'login.html', {'login_form': login_form})

    def post(self, request):
        """登录请求"""
        # 接受数据
        # username = request.POST.get('username', "")
        # password = request.POST.get('password', "")

        # 校验数据
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
            return render(request, 'login.html', {'login_form': login_form, 'res':1})


# /users/logout
class LogoutView(View):
    """退出登录"""
    def get(self,request):
        # 接受用户
        user = request.user
        # 退出登录状态
        logout(request)
        return redirect(reverse('index'))