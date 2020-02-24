from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'
    # 修改后台管理的条目显示
    verbose_name = "用户"
