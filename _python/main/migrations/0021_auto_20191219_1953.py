# Generated by Django 2.2.9 on 2019-12-19 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20191219_1940'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='role',
            name='roles_authori_fd60c5_idx',
        ),
        migrations.RemoveIndex(
            model_name='role',
            name='roles_authori_12a7ac_idx',
        ),
        migrations.RemoveField(
            model_name='role',
            name='authorizable_id',
        ),
        migrations.RemoveField(
            model_name='role',
            name='authorizable_type',
        ),
    ]
