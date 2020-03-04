from django.shortcuts import render, reverse
from django.views.generic import View
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse

from apps.organization.models import CourseOrg, City
from apps.courses.models import Course
from apps.organization.forms import AddAskForm


# /org/add_ask
class AddAskView(View):
    """
    立即咨询
    """
    def post(self, request):
        """表单提交处理"""
        add_ask_form = AddAskForm(request.POST)
        if not add_ask_form.is_valid():
            # 验证错误-->将错误原因取出并返回
            for key, val in add_ask_form.errors.items():
                msg = val[0]
                key = key
                break
            return JsonResponse({'status': 'fail', 'msg': msg, 'key': key})

        # 处理业务：验证通过
        # 提交数据到数据库
        ask_user = add_ask_form.save(commit=True)
        return JsonResponse({'status': 'success'})





# /org/org_list
class OrgListView(View):
    """课程机构"""

    def get(self, request):
        """显示"""
        # 查询所有机构
        all_org = CourseOrg.objects.all()

        # 授课机构排序
        hot_orgs = all_org.order_by('-click_nums')[:3]

        # 获取根据那个字段排序
        sort = request.GET.get('sort', '')
        if sort == 'students':  # 根据学习人数排序
            all_org = CourseOrg.objects.all().order_by('-students')
        elif sort == 'courses':  # 根据课程数排序
            all_org = CourseOrg.objects.all().order_by('-course_nums')

        # 查询所有机构的数量
        len_org = CourseOrg.objects.count()
        # 查询所有地区
        all_city = City.objects.all()

        # 使用课程类别进行过滤
        category = request.GET.get('ct', '')  # 获取要筛选的课程类别
        if not category == '':
            # 查询数据
            all_org = all_org.filter(category=category)

        # 使用所在地区进行过滤
        city_id = request.GET.get('city', '')  # 获取要筛选的课程类别
        try:
            if not city_id == '':
                # 查询数据
                all_org = all_org.filter(city=int(city_id))
        except Exception:
            pass

        # 分页
        age = request.GET.get('age', '')  # 获取要筛选的课程类别
        try:
            age = int(age)
        except Exception:
            age = 1
        # 进行分页
        p = Paginator(all_org, 1)
        page = p.page(age)
        # 校验age是否为数值
        try:
            age = int(age)
        except Exception:
            return HttpResponseRedirect(reverse('org:org_list'))
        number = p.num_pages
        # 生成一个下面页码的迭代器
        page_list = []
        if number <= 5:  # 总页数小于５
            page_list = range(1, number + 1)
        elif age <= 3:  # 前三页
            page_list = range(1, 6)
        elif age >= number - 2:
            page_list = range(number - 4, number + 1)
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
            'category': category,
            'city_id': city_id,
            'sort': sort,
            'hot_orgs': hot_orgs,
        }

        return render(request, 'org-list.html', countext)
