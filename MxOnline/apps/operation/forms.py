from django import forms

from apps.operation.models import UserFavorite, CourseComments


class OpeColForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ['fav_id', 'fav_type']


class CourseCommentForm(forms.ModelForm):
    """评论提交验证表单"""
    class Meta:
        model = CourseComments
        fields = ['course', 'comments']