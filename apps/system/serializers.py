#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from .models import SysLog, SysPermission, SysRole, SysUser, WhiteBlackList, TLookupGroup, TDictionary
from rest_framework import serializers


# 数据字典序列化类
class TDictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TDictionary
        fields = "__all__"


# lookup管理序列化类
class TLookupGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TLookupGroup
        fields = ("id", "group_code", "group_name", "state", "parent_group_code")


# 系统白名单序列化类
class WhiteBlackListSerializer(serializers.ModelSerializer):
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = WhiteBlackList
        fields = ("id", "user_name", "role_type", "ip", "remarks", "update_time")


# 日志管理序列化类
class SysLogSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = SysLog
        fields = "__all__"


# 菜单管理序列化类
class SysPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysPermission
        fields = ("id", "description", "icon", "model_order", "parent_id", "url")


# 角色管理序列化类
class SysRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysRole
        fields = "__all__"


# 用户管理序列化类
class SysUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUser
        fields = ("id", "user_name", "nick_name", "password")
