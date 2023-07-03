#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from django.db import models
from datetime import datetime

# 支付平台
class TPayApi(models.Model):
    payment_code = models.CharField(unique=True, max_length=20, null=True)  # 平台编码
    payment_name = models.CharField(max_length=50, null=True)  # 平台名称
    state = models.IntegerField(null=True)  # 状态
    memberid = models.CharField(max_length=50, null=True)  # 商户ID
    api_key = models.CharField(max_length=2000, null=True)  # apikey
    http_url = models.CharField(max_length=100, null=True)  # 请求地址
    http_type = models.CharField(max_length=10, null=True)  # 请求方式
    notify_url = models.CharField(max_length=100, null=True)
    notify_type = models.CharField(max_length=16, null=True)  # 回调类型
    callback_url = models.CharField(max_length=100, null=True)
    query_url = models.CharField(max_length=100, null=True)
    sign_type = models.CharField(max_length=50, null=True)
    sign_format = models.CharField(max_length=2000, null=True)
    param_format = models.CharField(max_length=2000, null=True)
    verify_format = models.CharField(max_length=2000, null=True)
    remark = models.CharField(max_length=200, null=True)  # 备注
    attribute_1 = models.CharField(max_length=400, null=True)
    attribute_2 = models.CharField(max_length=400, null=True)
    attribute_3 = models.CharField(max_length=1000, null=True)
    attribute_4 = models.CharField(max_length=2000, null=True)
    attribute_5 = models.CharField(max_length=2000, null=True)
    create_user = models.CharField(max_length=20, null=True)
    update_user = models.CharField(max_length=20, null=True)
    udpate_time = models.DateTimeField()
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = 't_pay_api'


# 支付二维码
class TPayCode(models.Model):
    code = models.TextField()  # 付款二维码
    comment = models.CharField(max_length=50, null=True)  # 备注
    pay_code = models.CharField(max_length=50, null=True)  # 支付类型
    status = models.IntegerField()  # 状态

    class Meta:
        db_table = 't_pay_code'


# 支付通道
class TPayInfo(models.Model):
    payment_code = models.CharField(max_length=20, null=True)
    payment_name = models.CharField(max_length=50, null=True)  # 平台名称
    pay_code = models.CharField(max_length=255, null=True)  # 支付编码
    item_name = models.CharField(max_length=50, null=True)  # 支付类型名称
    item_code = models.CharField(max_length=50, null=True)
    pay_model = models.IntegerField()  # 支付设备
    icon = models.CharField(max_length=255, null=True)  # 图标名称
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # 比例/费用
    rate_type = models.IntegerField(null=True)  # 佣金类型
    state = models.IntegerField(null=True)  # 状态
    min_switch = models.CharField(max_length=4, null=True)  # 最小金额开关
    min_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True)  # 最小金额
    max_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True)  # 最大金额
    max_switch = models.CharField(max_length=4, null=True)  # 最大金额开关
    point_switch = models.CharField(max_length=4, null=True)  # 小数开关
    bank_code = models.CharField(max_length=32, null=True)
    create_user = models.CharField(max_length=20, null=True)
    update_user = models.CharField(max_length=20, null=True)
    udpate_time = models.DateTimeField()
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = 't_pay_info'


# 支付类型
class TLookupItem(models.Model):
    item_code = models.CharField(max_length=20, null=True)  # 类型编码
    item_name = models.CharField(max_length=50, null=True)  # 类型名称
    sort = models.IntegerField(null=True)  # 排序
    state = models.IntegerField(null=True)  # 状态
    group_code = models.CharField(max_length=20, null=True)
    parent_item_code = models.CharField(max_length=20, null=True)
    attribute_1 = models.CharField(max_length=100, null=True)
    attribute_2 = models.CharField(max_length=100, null=True)  # 最小金额
    attribute_3 = models.CharField(max_length=100, null=True)  # 最大金额
    attribute_4 = models.CharField(max_length=100, null=True)  # 图标
    attribute_5 = models.CharField(max_length=100, null=True)
    create_user = models.CharField(max_length=20, null=True)
    update_user = models.CharField(max_length=20, null=True)
    udpate_time = models.DateTimeField()
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = 't_lookup_item'

