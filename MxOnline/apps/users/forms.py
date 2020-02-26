from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, required=True)
    password = forms.CharField(min_length=4, required=True)


class CaptchaForm(forms.Form):
    mobile = forms.CharField(max_length=11, min_length=11)
    captcha = CaptchaField()