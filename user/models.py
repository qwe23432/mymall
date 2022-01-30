from datetime import datetime

from django.db import models

# Create your models here.
from seller.models import Staff


class User(models.Model):
    username = models.CharField(max_length=20, verbose_name="用户名")
    password = models.CharField(max_length=20, verbose_name="用户密码")
    email = models.CharField(max_length=20, null=True, verbose_name="用户邮箱")
    nickname = models.CharField(max_length=20, null=True, verbose_name="用户昵称")
    money = models.FloatField(max_length=20, null=True, verbose_name="用户余额")
    picture = models.CharField(max_length=100, null=True, verbose_name="用户头像")
    status = models.CharField(max_length=20, null=True, verbose_name="用户状态", choices=(
        ('0', "未登录"),
        ('1', "已登录"),
    ))
    buy_status = models.IntegerField(default=1, choices=(
        (0, "冻结购买权限"),
        (1, "正常"),
    ))


class His(models.Model):
    user = models.IntegerField(default=0, verbose_name="用户id")
    type = models.IntegerField(default=0, verbose_name="商品类型", choices=(
        (0, "空"),
        (1, "饮食"),
        (2, "家电"),
        (3, "数码"),
        (4, "清洁用品"),
        (5, "玩具"),
    ))
    time = models.DateTimeField(verbose_name="浏览时间", default=datetime.now)
    staff = models.ForeignKey(Staff, verbose_name="商品", on_delete=models.CASCADE, default=1)


class Expression(models.Model):
    name = models.CharField(max_length=20, verbose_name="商品名称")
    store = models.CharField(max_length=20, verbose_name="商店名称")
    staffid = models.IntegerField(default=0, verbose_name="商品id")
    userid = models.CharField(max_length=20, null=True, verbose_name="用户id")
    username = models.CharField(max_length=20, verbose_name="用户昵称")
    expression = models.CharField(max_length=300, null=True, verbose_name="评论内容")
    sellerid = models.CharField(max_length=20, null=True, verbose_name="卖家id")
    addtime = models.DateTimeField(default=datetime.now, null=True, verbose_name="评论时间")
    status = models.IntegerField(default=0, verbose_name="评论是否被回复", choices=(
        (1, "是"),
        (0, "否"),
    ))
    dell = models.IntegerField(default=1, verbose_name="删除评论", choices=(
        (0, "评论已被删除"),
        (1, "正常"),
    ))


class Address(models.Model):
    user = models.IntegerField(default=0, verbose_name="用户id")
    address = models.CharField(max_length=20, null=True, verbose_name="用户地址")


class K(models.Model):
    k = models.CharField(max_length=1, null=True)


class Order(models.Model):
    userid = models.CharField(max_length=20, verbose_name="用户id")
    user = models.CharField(max_length=20, verbose_name="用户昵称")
    staff = models.IntegerField(default=0, verbose_name="商品id")
    seller = models.IntegerField(default=0, verbose_name="卖家id")
    address = models.CharField(max_length=20, verbose_name="发货地址")
    status = models.IntegerField(default=0, verbose_name="订单状态", choices=(
        (0, "未发货"),
        (1, "已发货"),
        (2, "用户已确认收货"),
        (3, "申请退货"),
        (4, "已退货"),
    ))
    # 0未发货 1已发货 2退货 3已退货
    number = models.CharField(max_length=20, verbose_name="商品数目")
    price = models.FloatField(max_length=20, verbose_name="商品价格")
    store = models.CharField(max_length=20, verbose_name="商店名字")
    name = models.CharField(max_length=20, verbose_name="商品名字")
    pictere = models.CharField(max_length=100, verbose_name="商品图片")
    buy_number = models.IntegerField(default=1, verbose_name="购买数目")
    update = models.DateTimeField(auto_now=True, verbose_name="订单状态更新时间")


class Cart(models.Model):
    staff = models.IntegerField(default=0, verbose_name="商品id")
    seller = models.IntegerField(default=0, verbose_name="商家id")
    number = models.CharField(max_length=20, verbose_name="商品数目")
    price = models.FloatField(max_length=20, verbose_name="商品价格")
    store = models.CharField(max_length=20, verbose_name="商店名字")
    name = models.CharField(max_length=20, verbose_name="商品名字")
    pictere = models.CharField(max_length=100, verbose_name="商品图片")
    userid = models.IntegerField(default=0, verbose_name="用户id")
    status = models.IntegerField(default=0, verbose_name="购物车商品状态", choices=(
        (0, "未购买"),
        (1, "已购买"),
        (2, "已删除"),
    ))
    buy_number = models.IntegerField(default=1, verbose_name="购买数目")
