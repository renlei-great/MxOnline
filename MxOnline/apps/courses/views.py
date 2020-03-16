from django.shortcuts import render, reverse, redirect
from django.views import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from apps.courses.models import Course, CourseTag, Video
from utils.OrgUtils import judge_org_login
from apps.operation.models import UserCourse, CourseComments


class VideoView(LoginRequiredMixin, View):
    """
    公开课--》 开始学习页 --> 视屏页
    """
    login_url = '/users/login'

    def get(self, request, course_id, video_id):
        """视屏页面显示"""

        # 查出此课程并将点击数加1
        try:
            course = Course.objects.get(id=course_id)
            course.click_nums += 1
            course.save()
        except Exception:
            return HttpResponseRedirect(reverse('course:list'))

        # 资料下载
        resources = course.courseresource_set.all()

        # 和用户建立链接
        user_course = course.usercourse_set.filter(course=course, user=request.user)
        if not user_course:
            user_course = UserCourse(course=course, user=request.user)
            user_course.save()
            course.students += 1
            course.save()

        # 学习过该课的同学还学习过那些课程
        users_course = UserCourse.objects.filter(course=course)
        users_id = [user.user_id for user in users_course]
        user_course = UserCourse.objects.filter(user_id__in=users_id).order_by('-course__click_nums').exclude(
            course_id=course.id)

        # 去重
        distinct_set = set()
        all_user_course = []
        for cou in user_course:
            if cou.course_id not in distinct_set:
                distinct_set.add(cou.course_id)
                all_user_course.append(cou)

        # 此课程的所有章节
        cou_lesson = course.lesson_set.all()

        # 查询此章节小节
        try:
            video = Video.objects.get(id=int(video_id))
        except Exception:
            return HttpResponseRedirect(redirect('course:lesson'))

        # 组织模板上下文
        context = {
            'course': course,
            'cou_lesson': cou_lesson,
            'resources': resources,
            'all_user_course': all_user_course,
            'video': video,
        }

        # 返回数据
        return render(request, 'course-play.html', context)


class CourseCommentView(LoginRequiredMixin, View):
    """
    公开课--》 开始学习页 --> 评论页
    """
    login_url = '/users/login'

    def get(self, request, course_id):
        """评论页显示"""
        # 查出此课程并将点击数加1
        try:
            course = Course.objects.get(id=course_id)
            course.click_nums += 1
            course.save()
        except Exception:
            return HttpResponseRedirect(reverse('course:list'))

        # 资料下载
        resources = course.courseresource_set.all()

        # 和用户建立链接
        user_course = course.usercourse_set.filter(course=course, user=request.user)
        if not user_course:
            user_course = UserCourse(course=course, user=request.user)
            user_course.save()
            course.students += 1
            course.save()

        # 学习过该课的同学还学习过那些课程
        users_course = UserCourse.objects.filter(course=course)
        users_id = [user.user_id for user in users_course]
        user_course = UserCourse.objects.filter(user_id__in=users_id).order_by('-course__click_nums').exclude(
            course_id=course.id)

        # 去重
        distinct_set = set()
        all_user_course = []
        for cou in user_course:
            if cou.course_id not in distinct_set:
                distinct_set.add(cou.course_id)
                all_user_course.append(cou)

        # 此课程的所有评论
        course_comments = CourseComments.objects.filter(course=course)[::-1]

        # 组织模板上下文
        context = {
            'course': course,
            'resources': resources,
            'all_user_course': all_user_course,
            'course_comments': course_comments,
        }

        has_reverse = request.GET.get('has_reverse')


        return render(request, 'course-comment.html', context)


class CourseLessonView(LoginRequiredMixin, View):
    """
    公开课--》 开始学习页
    """
    login_url = '/users/login'

    def get(self, request, course_id):
        """开始学习页显示"""
        # 查出此课程并将点击数加1
        try:
            course = Course.objects.get(id=course_id)
            course.click_nums += 1
            course.save()
        except Exception:
            return HttpResponseRedirect(reverse('course:list'))

        # 资料下载
        resources = course.courseresource_set.all()

        # 和用户建立链接
        user_course = course.usercourse_set.filter(course=course, user=request.user)
        if not user_course:
            user_course = UserCourse(course=course, user=request.user)
            user_course.save()
            course.students += 1
            course.save()

        # 学习过该课的同学还学习过那些课程
        users_course = UserCourse.objects.filter(course=course)
        users_id = [user.user_id for user in users_course]
        user_course = UserCourse.objects.filter(user_id__in=users_id).order_by('-course__click_nums').exclude(
            course_id=course.id)

        # 去重
        distinct_set = set()
        all_user_course = []
        for cou in user_course:
            if cou.course_id not in distinct_set:
                distinct_set.add(cou.course_id)
                all_user_course.append(cou)

        # 此课程的所有章节
        cou_lesson = course.lesson_set.all()

        # 组织模板上下文
        context = {
            'course': course,
            'cou_lesson': cou_lesson,
            'resources': resources,
            'all_user_course': all_user_course,
        }

        has_reverse = request.GET.get('has_reverse')

        if has_reverse == '1':
            # 返回数据
            return render(request, 'course-video.html', context)
        else:
            return render(request, 'course-play.html', context)


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

        # 搜索功能
        # 获取要查询的字符串
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_course = Course.objects.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

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
            'option': 'course',
            'keywords': keywords
        }
        return render(request, 'course-list.html', context)


class CourseDetailView(View):
    """
    公开课--》 详情页
    """

    def get(self, request, course_id):
        """详情页显示"""
        # 查出此课程并将点击数加1
        try:
            course = Course.objects.get(id=course_id)
            course.click_nums += 1
            course.save()
        except Exception:
            return HttpResponseRedirect(reverse('course:list'))

        # 查看用户是否收藏过此课程
        has_collect_course = judge_org_login(request, course_id, 1)
        org_id = course.course_org.id
        has_collect_org = judge_org_login(request, org_id, 2)

        # 根据课程标签相关课程推荐
        tags = course.coursetag_set.all()  # 本课程的所有标签
        # 取出此课程的所有标签,为了达到多个标签无重复，这里使用集合数据结构
        tag_set = set()
        for tag in tags:
            tag_set.add(tag.tag)
        # 查询出带有标签tag_ste集合里标签
        all_tags = CourseTag.objects.filter(tag__in=tag_set).exclude(course__id=course.id)
        # 取粗这些标签中的所有课程，放到tag_courses中
        tag_courses = []
        # 遍历取出
        for cou in all_tags[:3]:
            tag_courses.append(cou.course)

        # 组织模板上下文
        context = {
            'course': course,
            'has_collect_course': has_collect_course,
            'has_collect_org': has_collect_org,
            'org_id': org_id,
            'tag_courses': tag_courses,
        }

        # 返回数据
        return render(request, 'course-detail.html', context)
