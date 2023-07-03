#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from rest_framework import serializers
from .models import TOrderHis, TOrder


# 历史订单列表序列化类
class TOrderHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TOrderHis
        fields = "__all__"


# 待处理订单表序列化类
class TOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TOrder
        fields = "__all__"
