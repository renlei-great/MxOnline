from django import forms
from captcha.fields import CaptchaField
import redis

from apps.users.models import UserProfile


class UpdatePwsForm(forms.Form):
    password1 = forms.CharField(min_length=7, required=True, max_length=20)
    password2 = forms.CharField(min_length=7, required=True, max_length=20)

    def clean(self):
        pwd1 = self.cleaned_data.get('password1', '1')
        pwd2 = self.cleaned_data.get('password2', '2')

        if pwd2 != pwd1:
            raise forms.ValidationError('两次密码不一致')

        return self.cleaned_data


class UploadInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True)
    code = forms.CharField(min_length=4, max_length=4, required=True)
    password = forms.CharField(required=True)

    def clean_mobile(self):
        # 获取数据
        mobile = self.cleaned_data['mobile']
        # 查询是否被注册过
        user = UserProfile.objects.filter(mobile=mobile)
        # 判断
        if user:
            raise forms.ValidationError('该手机号码已经注册过')

        # 返回数据
        return mobile

    def clean_code(self):
        # 获取数据
        mobile = self.data['mobile']
        code = self.data['code']

        # 连接数据库：取出ｃｏｄｅ的值
        redis_cli = redis.Redis()
        try:
            redis_code = redis_cli.get(mobile)  # 取出数据库中的ｃｏｄｅ
            redis_code = redis_code.decode()
        except AttributeError:
            redis_code = 'aaaa'

        # 校验手机验证码
        if redis_code != code:
            # 验证码输入不正确
            raise forms.ValidationError('手机验证码输入不正确')

        return code

    # def errors(self):
    #     errors = {}
    #     for key, val in self.errors.items:
    #         errors[key] = val[1]
    #         break
    #
    #     return errors


class UpdateMobileForm(forms.Form):
    """修改手机号"""
    captcha = CaptchaField()


class RegisterForm(forms.Form):
    captcha = CaptchaField()


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, required=True)
    password = forms.CharField(min_length=4, required=True)


class CaptchaForm(forms.Form):
    mobile = forms.CharField(max_length=11, min_length=11)
    captcha = CaptchaField()


class MobileLoginForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True)
    code = forms.CharField(min_length=4, max_length=4, required=True)

    def clean_code(self):
        # 获取数据
        mobile = self.data['mobile']
        code = self.data['code']

        # 连接数据库：取出ｃｏｄｅ的值
        redis_cli = redis.Redis()
        try:
            redis_code = redis_cli.get(mobile)  # 取出数据库中的ｃｏｄｅ
            redis_code = redis_code.decode()
        except AttributeError:
            redis_code = 'aaaa'

        # 校验手机验证码
        if redis_code != code:
            # 验证码输入不正确
            raise forms.ValidationError('手机验证码输入不正确')

        return self.cleaned_data





