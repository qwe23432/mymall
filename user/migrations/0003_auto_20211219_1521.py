# Generated by Django 2.2.24 on 2021-12-19 15:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20211219_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='his',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 19, 15, 21, 20, 287895), verbose_name='浏览时间'),
        ),
    ]
