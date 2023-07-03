#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from rest_framework import serializers
from .models import TCustomerUser, TGroup


# 会员列表序列化类
class TCustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TCustomerUser
        fields = ("id", "user_account", "group_id")


# 会员分级序列化类
class TGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TGroup
        fields = ("id", "name", "str_values")
        extra_kwargs = {
            # "str_values": {'read_only': True}
        }

