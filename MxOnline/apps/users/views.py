from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect, JsonResponse
# from django.urls import reverse
from apps.users.forms import LoginForm, CaptchaForm


from MxOnline.settings import APIKEY
from utils import RandomStr, YunPian

# /users/send_sms/
class SendSmsView(View):
    """发送手机验证码"""
    def post(self, request):
        # 校验数据
        login_send_form = CaptchaForm(request.POST)

        # 验证数据是否通过，处理核心逻辑
        res_dict = {}
        if login_send_form.is_valid():
            # 验证通过
            # 组织数据
            mobile = login_send_form.cleaned_data['mobile']
            apikey = APIKEY
            andom = RandomStr.random_str(4)

            # 发送短信
            res_send = YunPian.send_captcha(apikey, mobile, andom)

            # 校验结果
            if res_send['code'] == '0':
                # 发送成功
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
    """登录页面"""
    def get(self, request):
        """登录页面显示"""
        user = request.user
        if user.is_authenticated:   # is_authenticated
            return redirect(reverse('index'))
        login_form = CaptchaForm(request.POST)

        return render(request, 'login.html', {'login_form': login_form})

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


# /users/logout
class LogoutView(View):
    """退出登录"""
    def get(self,request):
        # 接受用户
        user = request.user
        # 退出登录状态
        logout(request)
        return redirect(reverse('index'))