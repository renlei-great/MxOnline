from django.shortcuts import render
from django.views import View
from pure_pagination import Paginator, PageNotAnInteger

from apps.courses.models import Course


class CourseListView(View):
    """
    公开课--》 列表页
    """
    def get(self, request):
        """列表页显示"""
        # 对全部课程进行排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            # 最热门排序-click_nums
            all_course = Course.objects.all().order_by('-click_nums')
        elif sort is 'students':
            # 参与人数排序-students
            all_course = Course.objects.all().order_by('-students')
        else:
            # 最新排序-add_time
            all_course = Course.objects.all().order_by('-add_time')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对排序后的全部课程进行分页
        p = Paginator(all_course, per_page=2, request=request)
        page_course = p.page(page)

        # 组织模板上下文
        context = {
            'page_course': page_course,
            'active': 'course'
        }
        return render(request, 'course-list.html', context)
