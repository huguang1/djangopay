#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from django.db import models
from datetime import datetime


# 订单
class TOrder(models.Model):
    user_account = models.CharField(max_length=20, null=True)  # 用户名
    order_id = models.CharField(unique=True, max_length=255, null=True)  # 订单编码
    order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # 订单金额
    #  支付状态 INIT(0, "全部状态"), PAYING(10, "支付处理中"),PAY_FILED(20, "支付失败"), PAY_SUCCESS(30,"支付成功");
    order_state = models.IntegerField(null=True)  # 订单状态
    order_desc = models.CharField(max_length=255, null=True)
    order_time = models.DateTimeField(null=True)
    user_ip = models.CharField(max_length=50, null=True)
    payment_code = models.CharField(max_length=255, null=True)  # 订单来源
    pay_code = models.CharField(max_length=100, null=True)
    pay_order = models.CharField(max_length=255, null=True)
    item_code = models.CharField(max_length=255, null=True)  # 支付方式
    #  ALL(0, "全部状态"), OPE_TO_DO(10, "待处理"), OPE_LOCKED(20, "已锁定"), OPE_TO_CONFIRM(30, "待确认"),
    #  OPE_CONFIRM(40, "已确定" ),OPE_CANCEL(50, "已取消")
    state = models.IntegerField(null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # 手续费
    rate_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    lock_id = models.CharField(max_length=20, null=True)
    external_id = models.IntegerField(null=True)
    update_time = models.DateTimeField(null=True)
    update_user = models.CharField(max_length=30, null=True)
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def to_full_dict(self):
        to_dict = {
            "id": self.id,
            "user_account": self.user_account,
            "order_id": self.order_id,
            "order_amount": self.order_amount,
            "order_state": self.order_state,
            "order_desc": self.order_desc,
            "order_time": self.order_time,
            "user_ip": self.user_ip,
            "payment_code": self.payment_code,
            "pay_code": self.pay_code,
            "pay_order": self.pay_order,
            "item_code": self.item_code,
            "state": self.state,
            "rate": self.rate,
            "rate_amount": self.rate_amount,
            "lock_id": self.lock_id,
            "external_id": self.external_id,
            "update_time": self.update_time,
            "update_user": self.update_user,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return to_dict

    class Meta:
        db_table = 't_order'


# 每日订单统计
class TOrderDaliySum(models.Model):
    order_date = models.DateField(primary_key=True)
    number = models.IntegerField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order_state = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount_success = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    amount_fail = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    number_success = models.IntegerField(null=True)
    number_fail = models.IntegerField(null=True)
    on_pay_order_id = models.CharField(max_length=255, null=True)
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = 't_order_daliy_sum'


# 历史订单列表
class TOrderHis(models.Model):
    user_account = models.CharField(max_length=20, null=True)  # 用户名
    order_id = models.CharField(unique=True, max_length=255, null=True)  # 订单编码
    order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # 订单金额
    order_state = models.IntegerField(null=True)  # 订单状态
    order_desc = models.CharField(max_length=255, null=True)
    order_time = models.DateTimeField()
    user_ip = models.CharField(max_length=50, null=True)
    payment_code = models.CharField(max_length=255, null=True)  # 订单来源
    pay_code = models.CharField(max_length=100, null=True)
    pay_order = models.CharField(max_length=255, null=True)
    item_code = models.CharField(max_length=255, null=True)  # 支付方式
    state = models.IntegerField(null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # 手续费
    rate_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    lock_id = models.CharField(max_length=20, null=True)
    update_time = models.DateTimeField()
    update_user = models.CharField(max_length=30, null=True)
    batch_no = models.IntegerField()
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def to_full_dict(self):
        toh_dict = {
            "id": self.id,
            "user_account": self.user_account,
            "order_id": self.order_id,
            "order_amount": self.order_amount,
            "order_state": self.order_state,
            "order_desc": self.order_desc,
            "order_time": self.order_time,
            "user_ip": self.user_ip,
            "payment_code": self.payment_code,
            "pay_code": self.pay_code,
            "pay_order": self.pay_order,
            "item_code": self.item_code,
            "state": self.state,
            "rate": self.rate,
            "rate_amount": self.rate_amount,
            "lock_id": self.lock_id,
            "update_time": self.update_time,
            "update_user": self.update_user,
            "batch_no": self.batch_no,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return toh_dict

    class Meta:
        db_table = 't_order_his'
