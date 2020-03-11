from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse

from apps.operation.forms import CourseCommentForm
from apps.operation.forms import OpeColForm
from apps.operation.models import UserFavorite, CourseComments
from utils import OrgUtils


class OpeColView(View):
    """
    用户相关操作--> 收藏处理
    """

    def post(self, request):
        """机构收藏处理"""
        # 获取用户
        user = request.user
        if not user.is_authenticated:
            # 用户未登录
            return JsonResponse({'msg': '用户未登录', 'status': 'fail'})

        # 验证数据
        ope_col_form = OpeColForm(request.POST)
        if not ope_col_form.is_valid():
            # 参数出错
            return JsonResponse({'msg': '参数出错', 'status': 'fail'})

        # 处理业务
        # 获取数据
        fav_type = ope_col_form.cleaned_data['fav_type']
        fav_id = ope_col_form.cleaned_data['fav_id']

        # 查出当前用户是否收藏过此机构
        try:
            user_fav = UserFavorite.objects.get(user=user, fav_id=fav_id, fav_type=fav_type)
            is_user_fav_col = True
        except UserFavorite.DoesNotExist:
            is_user_fav_col = False

        if is_user_fav_col:  # 收藏过此机构
            # 取消收藏此机构
            user_fav.delete()
            # 在此收藏类型中减一
            OrgUtils.utils_collect(fav_type, fav_id, 'cancel')
        else:  # 未收藏过
            user_fav = UserFavorite()
            user_fav.user = user
            user_fav.fav_id = fav_id
            user_fav.fav_type = fav_type
            user_fav.save()
            OrgUtils.utils_collect(fav_type, fav_id, 'add')

        # 返回数据
        return JsonResponse({'status': 'success', 'res': fav_type})


class OpeCommentView(View):
    """
    公开课--》 开始学习页 --> 评论页提交
    """

    def post(self, request):
        """提交评论"""

        # 验证表单数据
        course_comment_from = CourseCommentForm(request.POST)
        if course_comment_from.is_valid():
            # 获取数据
            course = course_comment_from.cleaned_data['course']  # 这里直接返回了课程对象
            comment = course_comment_from.cleaned_data['comments']
            # 获取到评论模板对象进行赋值
            comments = CourseComments()
            comments.user = request.user
            comments.comments = comment
            comments.course = course
            comments.save()

            # 返回数据
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '参数错误'})
