# Generated by Django 2.2.24 on 2021-12-19 15:28
from datetime import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20211219_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='his',
            name='time',
            field=models.DateTimeField(default=datetime.now, verbose_name='浏览时间'),
        ),
        migrations.CreateModel(
            name='K',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('k', models.CharField(max_length=1, null=True)),
            ],
        ),
    ]