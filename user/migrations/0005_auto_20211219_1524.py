# Generated by Django 2.2.24 on 2021-12-19 15:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20211219_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='his',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='浏览时间'),
        ),
    ]