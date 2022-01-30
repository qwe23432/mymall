# Generated by Django 2.2.24 on 2021-12-12 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0015_auto_20211207_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='do_status',
            field=models.IntegerField(choices=[(0, '冻结'), (1, '正常')], default=1, verbose_name='订单处理权限'),
        ),
        migrations.AddField(
            model_name='staff',
            name='type',
            field=models.IntegerField(choices=[(1, '饮食'), (2, '家电'), (3, '数码'), (4, '清洁用品'), (5, '玩具')], default=1, verbose_name='商品类型'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='expressionid',
            field=models.IntegerField(null=True, verbose_name='原帖id'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='status',
            field=models.IntegerField(choices=[(1, '正常'), (2, '缺货'), (3, '已删除'), (4, '下架')], default=4, verbose_name='商品状态'),
        ),
    ]
