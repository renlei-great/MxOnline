# Generated by Django 2.2 on 2020-03-20 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_is_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerCorse',
            fields=[
            ],
            options={
                'verbose_name': '课程轮播',
                'verbose_name_plural': '课程轮播',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('courses.course',),
        ),
    ]
