from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ("male", '男'),
        ("female", "女")
    )

    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")  # default默认值
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)  # null  and  blank  容许为空
    gender = models.CharField(verbose_name="性别", choices=GENDER_CHOICES, max_length=6)  # choices　固定选项
    address = models.CharField(max_length=100, verbose_name="地址", default="")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")  # unique　字段是唯一的
    image = models.ImageField(upload_to="head_image/%Y/%m", default="default.jpg", verbose_name="头像")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username
