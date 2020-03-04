from django.shortcuts import render, reverse
from django.views.generic import View
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from apps.organization.models import CourseOrg, City
from apps.courses.models import Course


# /org/org_list
class OrgListView(View):
    """课程机构"""
    def get(self, request, age):
        """显示"""
        # 查询所有机构
        all_org = CourseOrg.objects.all()
        # 查询所有机构的数量
        len_org = CourseOrg.objects.count()

        # 查询所有地区
        all_city = City.objects.all()

        # 分页
        p = Paginator(all_org, 1)
        page = p.page(age)
        # 校验age是否为数值
        try:
            age = int(age)
        except Exception:
            return HttpResponseRedirect(reverse('org:org_list'))
        number = p.num_pages
        page_list = []
        if number <= 5:  # 总页数小于５
            page_list = range(1, number+1)
        elif age <= 3:  # 前三页
            page_list = range(1, 6)
        elif age >= number - 2:
            page_list = range(number-4, number+1)
        else:
            page_list = range(age - 2, age + 3)

        # 动态添加属性--> 课程机构下的课程
        for org in page:
            # 查询每个机构的所有课程

            courses = Course.objects.filter(course_org=org, is_classics=True)[0:3]
            org.courses = courses

            # 组织数据
        countext = {
            'all_org': all_org,
            'len_org': len_org,
            'page': page,
            'page_list': page_list,
            'age': age,
            'all_city': all_city,
        }

        return render(request, 'org-list.html', countext)
