# Generated by Django 2.2.24 on 2021-12-07 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0012_auto_20211207_0742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='staffid',
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(max_length=1000, verbose_name='介绍内容'),
        ),
    ]