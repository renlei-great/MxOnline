from django.shortcuts import render, reverse
from django.views import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponseRedirect

from apps.courses.models import Course
from utils.OrgUtils import judge_org_login


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
        elif sort == 'students':
            # 参与人数排序-students
            all_course = Course.objects.all().order_by('-students')
        else:
            # 最新排序-add_time
            all_course = Course.objects.all().order_by('-add_time')

        # 热门课程推荐
        click_course = Course.objects.all().order_by('-click_nums')[:3]

        # 分页
        try:
            page = request.GET.get('page', 1)
            page = int(page)
        except Exception:
            page = 1

        # 对排序后的全部课程进行分页
        p = Paginator(all_course, per_page=2, request=request)
        page_course = p.page(page)

        # 组织模板上下文
        context = {
            'page_course': page_course,
            'click_course': click_course,
            'sort': sort,
        }
        return render(request, 'course-list.html', context)


class CourseDetailView(View):
    """
    公开课--》 详情页
    """
    def get(self, request, course_id):
        """详情页显示"""
        # 查出此课程
        try:
            course = Course.objects.get(id=course_id)
        except Exception:
            return HttpResponseRedirect(reverse('course:list'))

        # 查看用户是否收藏过此课程
        has_collect_course = judge_org_login(request, course_id, 1)
        org_id = course.course_org.id
        has_collect_org = judge_org_login(request, org_id, 2)

        # 组织模板上下文
        context = {
            'course': course,
            'has_collect_course': has_collect_course,
            'has_collect_org': has_collect_org,
            'org_id': org_id,
        }

        # 返回数据
        return render(request, 'course-detail.html', context)

