import re

from django import forms

from apps.operation.models import UserAsk


class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(max_length=11, min_length=11, required=True)

    class Meta():
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data['mobile']
        regex_mobile = "^1\d{10}$"
        r = re.compile(regex_mobile)
        if r.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法')

