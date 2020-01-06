# Generated by Django 2.2.9 on 2019-12-19 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20191219_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolesuser',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Role'),
        ),
        migrations.AlterField(
            model_name='rolesuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
