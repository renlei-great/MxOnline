from django.shortcuts import render, reverse
from django.views.generic import View
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from apps.organization.models import CourseOrg, City, Teacher
from apps.courses.models import Course
from apps.organization.forms import AddAskForm
from utils.OrgUtils import judge_org_login


# /org/teacher_detail
class TeacherDetailView(View):
    """
    授课讲师 --> 详情页
    """
    def get(self, request, teacher_id):
        """详情页显示"""
        # 查询出此教师
        try:
            teacher = Teacher.objects.get(id=int(teacher_id))
        except Exception:
            return HttpResponseRedirect(reverse('org:teacher_list'))

        # 讲师排行傍
        order_all_teacher = Teacher.objects.all().order_by('-work_years')[:5]

        # 查询出此教师所属的机构
        org = teacher.org

        # 查询此教师下的所有课程
        teacher_all_course = teacher.course_set.all()

        # 使用自定义工具查看用户时候收藏过当前机构和课程
        has_collect_teacher = judge_org_login(request, teacher.id, 3)
        has_collect_org = judge_org_login(request, org.id, 2)

        # 组织模板上下文
        context = {
            "org": org,
            'order_all_teacher': order_all_teacher,
            'teacher': teacher,
            'teacher_all_course': teacher_all_course,
            'has_collect_org': has_collect_org,
            'has_collect_teacher': has_collect_teacher,
        }

        # 返回数据
        return render(request, 'teacher-detail.html', context)


# /org/teacher_list
class TeacherListView(View):
    """
    授课教师 --> 列表页
    """
    def get(self, request):
        """列表页显示"""
        # 查询出所有教师
        all_teacher = Teacher.objects.all()
        # 查询共有多少教师
        all_teacher_num = all_teacher.count()
        # 使用什么字段进行排序
        sort = request.GET.get('sort', "")

        if sort == 'hot':
            all_teacher = all_teacher.order_by('-click_nums')

        # 对所有教师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 创建paginator对象对教师进行分页
        p = Paginator(all_teacher, per_page=1, request=request)
        page_teacher = p.page(page)

        # 根据点击数对讲师进行排序
        order_all_teacher = all_teacher.order_by('-work_years')[:5]

        # 组织模板上下文
        context = {
            'page_teacher': page_teacher,
            'order_all_teacher': order_all_teacher,
            'all_teacher_num': all_teacher_num,
            'page': page,
            'sort': sort,
        }

        # 返回数据
        return render(request, 'teachers-list.html', context)


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
        # 引入以前学的分页模板
        from django.core.paginator import Paginator

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


# /org/home
class DetailHomeView(View):
    """
    课程机构－－>机构首页
    """
    def get(self, request, org_id):
        """显示课程机构主页"""
        # 校验数据
        try:
            org_id = int(org_id)
        except Exception:
            return HttpResponseRedirect(reverse('org:org_list'))

        # 处理业务
        # 点击次数加１
        try:
            org = CourseOrg.objects.get(id=org_id)
        except CourseOrg.DoesNotExist:
            return HttpResponseRedirect(reverse('org:org_list'))

        org.click_nums += 1
        org.save()

        # 全部课程查询,取前四
        portion_course = org.course_set.all()[:4]

        # 查询全部教师，取一个
        try:
            portion_teacher = org.teacher_set.all()[0]
            teacher_none = False
        except IndexError:
            teacher_none = True
            portion_teacher = None

        # 检查用户是否登录，是否关注过此机构
        judge_collect = judge_org_login(request, org_id, 2)

        # 组织上下文
        context = {
            'org': org,
            'portion_course': portion_course,
            'portion_teacher': portion_teacher,
            'teacher_none': teacher_none,
            'active': 'home',
            'judge_collect': judge_collect,
        }

        # 返回数据
        return render(request, 'org-detail-homepage.html', context)


# /org/teacher
class DetailTeacherView(View):
    """
    课程机构--> 机构讲师
    """
    def get(self, request, org_id):
        """显示机构讲师"""
        # 校验数据
        try:
            org_id = int(org_id)
        except Exception:
            return HttpResponseRedirect(reverse('org:org_list'))

        # 处理业务
        # 查询出课程机构
        try:
            org = CourseOrg.objects.get(id=org_id)
        except CourseOrg.DoesNotExist:
            return HttpResponseRedirect(reverse('org:org_list'))
        # 查出此课程机构下的所有讲师
        teachers = org.teacher_set.all()

        # 检查用户是否登录，是否关注过此机构
        judge_collect = judge_org_login(request, org_id, 2)

        # 组织上下文
        context = {
            'teachers': teachers,
            'active': 'teacher',
            'org': org,
            'judge_collect': judge_collect,
        }

        # 返回数据
        return render(request, 'org-detail-teachers.html', context)


# /org/course
class DetailCourseView(View):
    """
    课程机构--> 机构课程
    """
    def get(self, request, org_id):
        """机构页显示"""
        # 校验数据
        try:
            org_id = int(org_id)
        except Exception:
            return HttpResponseRedirect(reverse('org:org_list'))

        # 处理业务
        # 查询出课程机构
        try:
            org = CourseOrg.objects.get(id=org_id)
        except CourseOrg.DoesNotExist:
            return HttpResponseRedirect(reverse('org:org_list'))

        # 此机构下全部课程查询
        all_course = org.course_set.all()

        # 对前边课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 对课程分页  Paginator(分页集合, per_page=每页显示多少, request=request)
        p = Paginator(all_course, per_page=1, request=request)

        pag_course = p.page(page)

        # 检查用户是否登录，是否关注过此机构
        judge_collect = judge_org_login(request, org_id, 2)

        # 组织上下文
        context = {
            'pag_course': pag_course,
            'active': 'course',
            'org': org,
            'judge_collect': judge_collect,
        }

        # 返回数据
        return render(request, 'org-detail-course.html', context)


# /org/desc
class DetailDescView(View):
    """
    课程机构--> 机构介绍
    """
    def get(self, request, org_id):
        """显示机构介绍
        render-Prama： org,
        """
        # 校验数据
        try:
            org_id = int(org_id)
        except Exception:
            return HttpResponseRedirect(reverse('org:org_list'))

        # 处理业务
        # 查询出课程机构
        try:
            org = CourseOrg.objects.get(id=org_id)
        except CourseOrg.DoesNotExist:
            return HttpResponseRedirect(reverse('org:org_list'))

        # 检查用户是否登录，是否关注过此机构
        judge_collect = judge_org_login(request, org_id, 2)

        # 返回数据
        return render(request, 'org-detail-desc.html', {'org': org, 'judge_collect': judge_collect})







