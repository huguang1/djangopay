#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from rest_framework import serializers
from .models import TPayCode, TLookupItem, TPayApi, TPayInfo


# 支付二维码序列化类
class TPayCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPayCode
        fields = ("id", "code", "comment", "pay_code", "status")


# 支付类型序列化类
class TLookupItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TLookupItem
        fields = ("id", "attribute_1", "attribute_2", "attribute_3", "attribute_4", "group_code", "item_code",
                  "item_name", "sort", "state")


# 支付平台序列化类
class TPayApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPayApi
        fields = ("id", "api_key", "attribute_1", "attribute_2", "attribute_3", "attribute_4", "attribute_5",
                  "callback_url", "http_type", "http_url", "memberid", "notify_type", "notify_url", "param_format",
                  "payment_code", "payment_name", "query_url", "remark", "sign_format", "sign_type", "state",
                  "verify_format")


# 支付通道序列化类
class TPayInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TPayInfo
        fields = ("id", "bank_code", "item_code", "max_amount", "max_switch", "min_amount", "min_switch", "pay_code",
                  "payment_code", "point_switch", "rate", "rate_type", "state", "pay_model", "item_name", "icon",
                  "payment_name")
