# Generated by Django 2.2.24 on 2021-12-19 15:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20211219_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='his',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 19, 15, 22, 57, 688509), verbose_name='浏览时间'),
        ),
    ]