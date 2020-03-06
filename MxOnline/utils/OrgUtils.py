
from apps.operation.models import UserFavorite
from apps.organization.models import CourseOrg, Teacher
from apps.courses.models import Course


def judge_org_login(request, org_id):
    """
    检查是否由用户登录，判断是否关注过此机构
    :param request:
    :param org_id:
    :return:
    """
    user = request.user
    if not user.is_authenticated:
        # 用户未登录
        return False

    # 查询用户是否收藏过此机构
    user_fav = UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=org_id)
    if user_fav:
        return True
    else:
        return False


def utils_collect(fav_type, id, ope):
    """
    用户点击收藏按钮后的一系列收藏操作
    :param fav_type:  收藏类型
    :param id:   收藏id
    :param ope:  操作类型
    :return:
    """
    if fav_type == 1:
        fa = Course.objects.get(id=id)
    elif fav_type == 2:
        fa = CourseOrg.objects.get(id=id)
    else:
        fa = Teacher.objects.get(id=id)
    if ope == 'cancel':
        fa.fav_nums -= 1
    elif ope == 'add':
        fa.fav_nums += 1
    fa.save()