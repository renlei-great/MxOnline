# Generated by Django 2.2 on 2020-03-03 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20200303_2255'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='课程机构'),
        ),
        migrations.AddField(
            model_name='course',
            name='is_classics',
            field=models.BooleanField(default=True, verbose_name='是否经典'),
        ),
    ]
