import xadmin
from xadmin.layout import Fieldset, Main, Side, Row, FormHelper
from import_export import resources

from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag, BannerCorse




class CommSttings(object):

    site_title = "千华教育管理系统"
    site_footer = "千华教育平台"
    menu_style = "accordion"


class BaseSttings(object):
    enable_themes = True
    use_bootswatch = True


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'teacher']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]


class BannerCorseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'teacher']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]

    def queryset(self):  # 对同一张表实现不同后台管理器
        qs = super().queryset()  # 查询出这个表中的所有字段
        # 查询出时广告位的课程
        qs = qs.filter(is_banner=True)
        return qs


class CourseTagInline:
    """关联课程编辑页，一次性编辑多张表"""
    model = CourseTag
    extra = 1  # 打开这个页面时新增几个
    style = "tab"
    exclude = ["add_time"]  # 隐藏此字段


class LessonInline:
    """给课程页关联课程章节页，可以一次性编辑多张表"""
    model = Lesson
    extra = 1
    style = "tab"
    exclude = ["add_time"]


class MyResource(resources.ModelResource):
    """导入导出的类"""
    class Meta:
        model = Course
        # fields = ('name', 'description',)
        # exclude = ()


class NewCourseAdmin(object):
    # xadmin的导入导出
    import_export_args = {'import_resource_class': MyResource, 'export_resource_class': MyResource}

    list_display = ['name', 'desc','show_image','go_to_course', 'detail', 'degree', 'learn_times', 'students', 'teacher']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]
    readonly_fields = ['students', 'fav_nums', 'click_nums']
    exclude = ['add_time']
    ordering = ['-students']
    model_icon = 'fa fa-map-o'
    inlines = [CourseTagInline, LessonInline]
    style_fields = {
        "detail": "ueditor"  # detail表示此模型类的那个字段时富文本
    }


    def queryset(self):  # 控制对数据的过滤
        qs = super().queryset()
        if not self.request.user.is_superuser:
            teacher = self.request.user.teacher
            qs = qs.filter(teacher=self.request.user.teacher)
        pass
        return qs

    def get_form_layout(self):  # 修改显示布局
        if self.org_obj:
            # 判断是否时新增，返回真则不是
            self.form_layout = (
                Main(  # 左侧显示
                    Fieldset('讲师信息',
                             'teacher', 'course_org',
                             css_class='unsort no_title'
                             ),
                    Fieldset('基本信息',
                             'name', 'desc', 'notice', 'youneed_know', 'teacher_tell', 'detail',
                             Row('learn_times', 'degree'),
                             Row('category', 'tag'),
                             ),
                    ),
                Side(  # 右侧小框显示
                    Fieldset('访问信息',
                            'click_nums', 'students', 'fav_nums'
                             ),

                    Fieldset('是否选择',
                                'is_banner', 'is_classics'
                            ),
                    ),
            )
        return super(NewCourseAdmin, self).get_form_layout()


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']  # 如果时外键可以加两个下划线意思是这个外键中的某个字段re

    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(course__in=Course.objects.filter(teacher=self.request.user.teacher))
        return qs


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_time']

    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(course__in=Course.objects.filter(teacher=self.request.user.teacher))
        return qs

    def save_models(self):  # 重写后台管理调用save操作
        # 判断是否可以保存是不是此教师的课程
        obj = self.new_obj
        if obj.course.teacher.id is self.request.user.teacher.id:
            obj.save()


        # else:
            # raise ValueError("这不是当前{}教师的课程".format(self.request.user.teacher.name))


class CourseTagAdmin(object):
    list_display = ['course', 'tag', 'add_time']
    search_fields = ['course', 'tag']
    list_filter = ['course', 'tag', 'add_time']



xadmin.site.register(BannerCorse, BannerCorseAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Course, NewCourseAdmin)
xadmin.site.register(xadmin.views.CommAdminView, CommSttings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSttings)

