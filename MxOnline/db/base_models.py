from datetime import datetime

from django.db import models


class BaseModledb(models.Model):
    """模型抽象基类"""
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        # 说明这是一个抽象基类
        # 有了这个在ｍａｇｒａｔｅ时就不会生成一个表了
        abstract = True
