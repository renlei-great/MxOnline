import xadmin
from xadmin.layout import Fieldset, Main, Side, Row, FormHelper

from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag



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


class NewCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'teacher']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]

    def get_form_layout(self):
        if self.org_obj:
            # 判断是否时新增，返回真则不是
            self.form_layout = (
                Main(
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
                Side(
                    Fieldset('访问信息',
                            Row('students', 'fav_nums'),
                            'click_nums', 'add_time',
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
    list_filter = ['course__name', 'name', 'add_time']  # 如果时外键可以加两个下划线意思是这个外键中的某个字段


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_time']


class CourseTagAdmin(object):
    list_display = ['course', 'tag', 'add_time']
    search_fields = ['course', 'tag']
    list_filter = ['course', 'tag', 'add_time']


xadmin.site.register(CourseTag, CourseTagAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Course, NewCourseAdmin)
xadmin.site.register(xadmin.views.CommAdminView, CommSttings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSttings)

