#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from django.db import models
from datetime import datetime


# 会员列表
class TCustomerUser(models.Model):
    user_account = models.CharField(unique=True, max_length=20, null=True)  # 会员账号
    level = models.IntegerField(null=True)
    amounts = models.DecimalField(max_digits=13, decimal_places=2, null=True)
    group_id = models.IntegerField(null=True)  # 级别编号
    remark = models.CharField(max_length=255, null=True)
    update_time = models.DateTimeField()
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = 't_customer_user'


# 会员分级
class TGroup(models.Model):
    name = models.CharField(max_length=50, null=True)  # 分级名称
    state = models.IntegerField(null=True)
    str_values = models.CharField(max_length=1000, null=True)  # 支持的付款方式
    remark = models.CharField(max_length=100,  null=True)
    create_user = models.CharField(max_length=20, null=True)
    update_user = models.CharField(max_length=20, null=True)
    update_time = models.DateTimeField()
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        managed = False
        db_table = 't_group'


# bbin订单类
class TGamePlatFormOrder(models.Model):
    number = models.CharField(max_length=255, null=True)
    order_id = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    created_at = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, null=True)
    notify_url = models.CharField(max_length=255, null=True)
    method_id = models.CharField(max_length=255, null=True)
    bank_id = models.CharField(max_length=255, null=True)
    sign = models.CharField(max_length=255, null=True)
    status = models.IntegerField(null=True)
    notify_time = models.DateTimeField()
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = 't_game_platform_order'
