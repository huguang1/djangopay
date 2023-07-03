#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# 日志管理
class SysLog(models.Model):
    log_ip = models.CharField(max_length=50, null=True)  # IP
    business = models.CharField(max_length=50, null=True)  # 日志内容
    log_user = models.CharField(max_length=50, null=True)  # 操作人
    model = models.CharField(max_length=50, null=True)   # 模块
    log_params = models.CharField(max_length=2000, null=True)  # 参数
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = 'sys_log'


# 菜单管理
class SysPermission(models.Model):
    # 权限路径
    url = models.CharField(max_length=100)  # 菜单地址
    # 描述
    description = models.CharField(max_length=100, null=True)  # 菜单名称
    # permission_id
    pid = models.IntegerField(null=True)
    # 菜单图标
    icon = models.CharField(max_length=255, null=True)  # 菜单图标
    # 菜单排序
    model_order = models.IntegerField(null=True)  # 菜单排序
    # 菜单分级(1:1级菜单;2:2级菜单;3:3级菜单)
    model_level = models.IntegerField(null=True)
    # 父级菜单id
    parent_id = models.IntegerField(null=True)
    # 有子菜单(1:有;0:无)
    has_child = models.IntegerField(null=True)
    # 路径类型（1:菜单;2:button;3:路径）
    permission_type = models.IntegerField(null=True)
    # 创建人
    create_user = models.CharField(max_length=100, null=True)
    # 更新时间
    update_time = models.DateTimeField()
    # 更新人
    update_user = models.CharField(max_length=100, null=True)

    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = 'sys_permission'


# 角色管理
class SysRole(models.Model):
    role_name = models.CharField(max_length=20, null=True)  # 角色名称
    role_desc = models.CharField(max_length=20, null=True)  # 角色描述

    class Meta:
        db_table = 'sys_role'


# 外键表
class SysRolePermission(models.Model):
    role_id = models.IntegerField()
    pers_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'sys_role_permission'


# 用户管理
class SysUser(AbstractUser):
    user_name = models.CharField(unique=True, max_length=100, null=True)  # 用户名
    nick_name = models.CharField(max_length=100, null=True)  # 昵称
    password = models.CharField(max_length=100, null=True)  # 密码
    last_login_time = models.DateTimeField(null=True)  # 上次登陆时间
    login_ip = models.CharField(max_length=255, null=True)  # 登陆IP
    level = models.IntegerField(null=True)
    state = models.IntegerField(null=True)
    update_time = models.DateTimeField()
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = 'sys_user'


# 外键表
class SysUserRole(models.Model):
    user_id = models.IntegerField(null=True)
    role_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'sys_user_role'


# 系统白名单
class WhiteBlackList(models.Model):
    ip = models.CharField(max_length=255, null=True)  # IP地址
    user_name = models.CharField(max_length=255, null=True)  # 会员名称
    role_type = models.IntegerField(null=True)
    remarks = models.CharField(max_length=255, null=True)  # 备注
    create_user = models.CharField(max_length=255, null=True)
    update_time = models.DateTimeField(null=True)
    update_user = models.CharField(max_length=255, null=True)
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = 'white_black_list'


# LOOKUP管理
class TLookupGroup(models.Model):
    group_code = models.CharField(unique=True, max_length=20, null=True)  # 编码
    group_name = models.CharField(unique=True, max_length=50, null=True)  # 名称
    state = models.IntegerField(null=True)  # 状态
    parent_group_code = models.CharField(max_length=50, null=True)  # 父ID
    create_user = models.CharField(max_length=20, null=True)
    update_user = models.CharField(max_length=20, null=True)
    udpate_time = models.DateTimeField()
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = 't_lookup_group'


# 数据字典
class TDictionary(models.Model):
    dic_key = models.CharField(max_length=255, null=True)  # 字典key
    dic_value = models.CharField(max_length=255, null=True)  # 字典值
    description = models.CharField(max_length=255, null=True)  # 字典描述

    class Meta:
        db_table = 't_dictionary'

