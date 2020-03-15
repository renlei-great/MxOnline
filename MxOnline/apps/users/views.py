from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect, JsonResponse
# from django.urls import reverse
import redis
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination import Paginator

from apps.users.forms import LoginForm, CaptchaForm, MobileLoginForm, RegisterForm, RegisterPostForm, UploadImageForm, UploadInfoForm, UpdatePwsForm, UpdateMobileForm
from MxOnline.settings import APIKEY
from utils import RandomStr, YunPian
from apps.users.models import UserProfile
from apps.operation.models import UserFavorite, UserMessage, Banner
from apps.courses.models import CourseOrg, Teacher, Course


# 设置全局变量
def message_num(request):
    if request.user.is_authenticated:
        return {'message_read_num': request.user.read_num()}
    else:
        return {}


# /index
class IndexView(View):
    """
    首页
    """
    def get(self, request):
        """首页显示"""
        # 查询轮播图
        banners = Banner.objects.all().order_by('index')

        # 公开课程和广告课程
        banner_course = Course.objects.filter(is_banner=True)
        courses = Course.objects.all()[:6]

        # 查询课程机构
        orgs = CourseOrg.objects.all()[:15]

        # 组织模板上下文
        context = {
            "banners": banners,
            'banner_course': banner_course,
            'courses': courses,
            'orgs': orgs,
        }

        return render(request, 'index.html', context)


# /users/message
class UsersMessageView(LoginRequiredMixin, View):
    """
    个人中心－我的消息
    """
    def get(self, request):
        """我的消息显示"""
        # 查询出用户的个人消息
        # user_message = UserMessage.objects.filter(user=request.user)
        user_message = request.user.usermessage_set.all()

        for message in user_message:
            message.has_read = True
            message.save()

        # 分页
        # 分页
        try:
            page = request.GET.get('page', 1)
            page = int(page)
        except Exception:
            page = 1

        # 对排序后的全部课程进行分页
        p = Paginator(user_message, per_page=2, request=request)
        page_message = p.page(page)

        # 返回数据
        return render(request, 'usercenter-message.html', {'user_message': user_message, 'active': 'message', 'page_message': page_message})


# /users/fav_caurse
class MyFavCourseView(LoginRequiredMixin, View):
    """
    我的收藏－授课讲师
    """
    def get(self, request):
        """我的授课讲师显示"""
        # 根据用户查询出用户收藏机构
        user_fav_teacher = UserFavorite.objects.filter(user=request.user, fav_type=1)
        # 存放ｏｒｇ
        course_list = []
        for user_org in user_fav_teacher:
            # 遍历收藏的机构，根据机构ｉｄ查询出收藏机构
            org = Course.objects.get(id=user_org.fav_id)
            course_list.append(org)

        # 返回数据
        return render(request, 'usercenter-fav-course.html', {'course_list': course_list, 'active': 'fav_course'})


# /users/fav_teacher
class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我的收藏－授课讲师
    """
    def get(self, request):
        """我的授课讲师显示"""
        # 根据用户查询出用户收藏机构
        user_fav_teacher = UserFavorite.objects.filter(user=request.user, fav_type=3)
        # 存放ｏｒｇ
        teacher_list = []
        for user_org in user_fav_teacher:
            # 遍历收藏的机构，根据机构ｉｄ查询出收藏机构
            org = Teacher.objects.get(id=user_org.fav_id)
            teacher_list.append(org)

        # 返回数据
        return render(request, 'usercenter-fav-teacher.html', {'teacher_list': teacher_list, 'active': 'fav_teacher'})


# /users/fav_org
class MyFavOrgView(LoginRequiredMixin, View):
    """
    我的收藏--课程收藏
    """
    def get(self, request):
        """课程收藏显示"""
        # 根据用户查询出用户收藏机构
        user_fav_org = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # 存放ｏｒｇ
        org_list = []
        for user_org in user_fav_org:
            # 遍历收藏的机构，根据机构ｉｄ查询出收藏机构
            org = CourseOrg.objects.get(id=user_org.fav_id)
            org_list.append(org)

        # 返回数据
        return render(request, 'usercenter-fav-org.html', {'org_list': org_list, 'active': 'fav_org'})


#  /users/update_mobile
class UpdateMobileView(LoginRequiredMixin, View):
    """修改手机号"""
    login_url = '/users/login'
    def post(self, request):
        """处理请求"""
        # 表单处理数据
        update_mobile_form = MobileLoginForm(request.POST)
        if not update_mobile_form.is_valid():
            return JsonResponse(update_mobile_form.errors)
        mobile = update_mobile_form.cleaned_data['mobile']
        if UserProfile.objects.filter(mobile=mobile):
            return JsonResponse({
                'mobile': '该手机号码已注册'
            })
        # 修改手机号码
        user = request.user
        user.mobile = mobile
        user.username = mobile
        user.save()

        # 返回数据
        return JsonResponse({
            'status': 'success'
        })


# /users/update_pwd
class UpdatePwdView(LoginRequiredMixin, View):
    """修改密码"""
    login_url = '/users/login'
    def post(self, request):
        """处理修改密码请求"""
        update_pwd_form = UpdatePwsForm(request.POST)
        if update_pwd_form.is_valid():
            pwd = request.POST.get('password1', "")
            user = request.user
            user.set_password(pwd)
            user.save()
            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse(update_pwd_form.errors)


# /users/upload_info
class UploadInfoView(LoginRequiredMixin, View):
    """个人资料"""
    login_url = '/users/login'
    def post(self,request):
        """修改个人资料"""
        login_url = '/users/login'
        # 交给forms处理表单数据
        upload_info_form = UploadInfoForm(request.POST, instance=request.user)
        if upload_info_form.is_valid():
            upload_info_form.save()
            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse(upload_info_form.errors)


# /users/upload_image
class UploadImageView(LoginRequiredMixin, View):
    """头像操作"""
    login_url = '/users/login'
    def post(self, request):
        """修改头像"""
        # 使用forms表单上传头像
        upload_image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if upload_image_form.is_valid():
            upload_image_form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({"status": 'fail'})


# /users/user_info
class UserInfoView(LoginRequiredMixin, View):
    """
    个人中心 --> 个人资料
    """

    def get(self, request):
        """个人资料显示"""
        mobile_form = UpdateMobileForm(request.POST)
        return render(request, 'usercenter-info.html', {'mobile_form': mobile_form, 'active': 'user_info'})


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

        # 登录成功删除用户刚才的验证码
        r = redis.Redis()
        r.delete(mobile)

        # 获取用户来前的页面
        url_next = request.GET.get('next', reverse('index'))

        # 返回首页
        return redirect(url_next)


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

        next = request.GET.get('next', '')

        return render(request, 'login.html', {'login_form': login_form, 'next': next})

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

                # 获取用户来前的页面
                url_next = request.GET.get('next', reverse('index'))

                # 返回首页
                return redirect(url_next)

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