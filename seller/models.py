from datetime import datetime

from django.db import models

# Create your models here.
from DjangoUeditor.DjangoUeditor.models import UEditorField


class Seller(models.Model):
    username = models.CharField(max_length=20, null=True, verbose_name="商家用户名")
    password = models.CharField(max_length=20, null=True, verbose_name="商家密码")
    type = models.IntegerField(null=True, verbose_name="经营类型", choices=(
        (1, "饮食"),
        (2, "家电"),
        (3, "数码"),
        (4, "清洁用品"),
        (5, "玩具"),
    ))
    # 1是饮食 2是家电 3是数码 4是清洁用品 5是玩具
    email = models.CharField(max_length=20, null=True, blank=True, verbose_name="商家邮箱")
    nickname = models.CharField(max_length=20, null=True, verbose_name="商家昵称")
    picture = models.CharField(max_length=100, null=True, verbose_name="商家头像")
    status = models.CharField(max_length=20, null=True, verbose_name="商家状态", choices=(
        ('0', "未登录"),
        ('1', "已登录")
    ))
    n = models.IntegerField(default=0, verbose_name="评论数")
    m = models.IntegerField(default=0, verbose_name="订单消息数")
    money = models.FloatField(default=0, verbose_name="赚的钱")
    do_status= models.IntegerField(default=1,verbose_name="订单处理权限",choices=(
        (0,"冻结"),
        (1,"正常")
    ))


class Store(models.Model):
    sellerid = models.CharField(max_length=20, null=True, verbose_name="商家id")
    name = models.CharField(max_length=20, null=True, verbose_name="商店名")
    picture = models.CharField(max_length=100, null=True, verbose_name="商店图片")


class Staff(models.Model):
    number = models.CharField(max_length=20, null=True, verbose_name="剩余数量")
    price = models.FloatField(max_length=20, null=True, verbose_name="价格")
    storeid = models.CharField(max_length=20, null=True, verbose_name="商店id")
    name = models.CharField(max_length=20, null=True, verbose_name="商店名字")
    messageid = models.CharField(max_length=20, null=True, verbose_name="介绍id")
    status = models.IntegerField(default=4, verbose_name="商品状态", choices=(
        (1, "正常"),
        (2, "缺货"),
        (3, "已删除"),
        (4, "下架"),
    ))
    # 1为正常 2为缺货 3为已删除
    pictere = models.CharField(max_length=100, null=True, verbose_name="商品图片")
    type = models.IntegerField(default=1, verbose_name="商品类型", choices=(
        (1, "饮食"),
        (2, "家电"),
        (3, "数码"),
        (4, "清洁用品"),
        (5, "玩具"),
    ))
    update=models.DateTimeField(auto_now=True,verbose_name="修改时间")


class Message(models.Model):
    message = UEditorField(max_length=1000, verbose_name="介绍内容")
    sellerid = models.CharField(max_length=20, null=True, verbose_name="商家Id")


class Reply(models.Model):
    seller = models.CharField(max_length=20, null=True, verbose_name="商家昵称")
    reply = models.CharField(max_length=50, null=True, verbose_name="回复内容")
    staffid = models.CharField(max_length=100, null=True, verbose_name="商品图片")
    expressionid = models.IntegerField(null=True, verbose_name="原帖id")
    addtime = models.DateTimeField(default=datetime.now, null=True, verbose_name="添加时间")
    username = models.CharField(max_length=20, null=True, verbose_name="买家昵称")
