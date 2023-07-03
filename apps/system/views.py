#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
import datetime
import hashlib
import io
import random
import uuid
import jwt
from PIL import Image, ImageDraw, ImageFont
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .models import SysUser, SysRole, SysUserRole, SysPermission, TDictionary, TLookupGroup, WhiteBlackList, SysLog, \
    SysRolePermission
from utils.constant import Constants
from utils.constant import SECRET
from utils.restful import result, forbidden, params_error, ok, server_error
from .serializers import TDictionarySerializer, TLookupGroupSerializer, WhiteBlackListSerializer, SysLogSerializer, \
    SysPermissionSerializer, SysRoleSerializer, SysUserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django_filters import rest_framework


# 验证码
class VerifyCodeView(View):
    def get(self, request):
        """
        这个验证码的功能是，后台生成随机数，保存在django的session中，同时将这个随机数做成图片，并增加一些噪点，
        传递给前端并展示出来。
        """
        # 定义变量，用于画面的背景色、宽、高
        bgcolor = '#3D1769'
        width = 100
        height = 40
        # 创建画面对象
        im = Image.new('RGB', (width, height), bgcolor)
        # 创建画笔对象
        draw = ImageDraw.Draw(im)
        # 调用画笔的point()函数绘制噪点
        for i in range(0, 100):
            xy = (random.randrange(0, width), random.randrange(0, height))
            fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
            draw.point(xy, fill=fill)
        # 定义验证码的备选值
        str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
        # 随机选取4个值作为验证码
        rand_str = ''
        for i in range(0, 4):
            rand_str += str1[random.randrange(0, len(str1))]
        # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
        font = ImageFont.truetype('FreeMono.ttf', 33)  # linux
        # font = ImageFont.truetype('arial.ttf', 33)  # win7的
        # 构造字体颜色
        # 选取验证码的背景颜色
        fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
        # 绘制4个字
        draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
        draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
        draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
        draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
        # 释放画笔
        del draw
        # 存入redis，用于做进一步验证
        cache.set(Constants["REDIS_CONFIG_CACHE_CODE"], rand_str, 60*10)
        # 内存文件操作
        buf = io.BytesIO()
        # 将图片保存在内存中，文件类型为png
        im.save(buf, 'png')
        response = HttpResponse(buf.getvalue())
        response['Content-type'] = 'image/png'
        # 将内存中的图片数据返回给客户端，MIME类型为图片png
        return response


# 获取验证登陆页面的token值
class GetConfigGetLoginToken(View):
    def post(self, request):
        num = random.randint(100000000, 999999999)
        payload = {'function': 'login', 'num': num, 'time': datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")}
        token = str(jwt.encode(payload, SECRET, algorithm='HS256'), encoding="utf-8")
        response = result(message="获取验证登陆页面的token值正确")
        # 这个登陆页面的token值的时间为五分钟
        response.set_cookie('loginToken', token, max_age=60*5)  # 这个是jwt加密后的token值，所以明文存储没有问题
        return response


# 登陆校验并返回token值
class GetLoginHandler(View):
    def post(self, request):
        cookieToken = request.COOKIES.get('loginToken')
        headerToken = self.request.headers["X-CSRF-TOKEN"]
        if cookieToken != headerToken:
            return forbidden(message="CSRF校验不能通过，请重试！")
        username = request.POST.get('username', '')
        password = request.POST.get('password', None)
        text = request.POST.get('text', None)
        redis_text = cache.get(Constants["REDIS_CONFIG_CACHE_CODE"])
        if not redis_text.lower() == text.lower():
            return params_error(message="验证码不正确，请重试")
        if not password:
            return params_error(message="密码不正确，请重试！")
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        password = hl.hexdigest()
        try:
            user = SysUser.objects.get(user_name=username, password=password)
            user_roles = SysUserRole.objects.filter(user_id=user.id)
            user_roles_id = [user_role.role_id for user_role in user_roles]
            roles = SysRole.objects.filter(id__in=user_roles_id)
            if not roles:
                return params_error(message="用户没有角色，请重试！")
            payload = {'function': 'usertoken', 'time': datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"), 'role': roles[0].role_desc, 'username': username}
            token = str(jwt.encode(payload, SECRET, algorithm='HS256'), encoding="utf-8")
            response = ok()
            response.set_cookie('token', token, max_age=60*30)
            # 设置用户的cookie信息
            session_id = uuid.uuid4().hex
            # 设置这个用户名的时间为半个小时
            response.set_cookie("session_id", session_id, max_age=60*30)
            # 将用户名存储在redis中
            cache.set('sess_%s' % session_id, username, 60*30)
            return response
        except SysUser.DoesNotExist as e:
            return params_error(message="用户不存在，请重试！")


# 获取登陆管理员
class GetUserNameHandler(View):
    def get(self, request):
        username = request.username
        return result(message=username)


# 获取到首页菜单
class MenuUuserMenuListHandler(View):
    def get(self, request):
        try:
            values = SysPermission.objects.filter(model_level=1).order_by('model_order')
            content = []
            for value in values:
                children = []
                childs = SysPermission.objects.filter(parent_id=value.id)
                for child in childs:
                    child_dict = {
                        "level": child.model_level,
                        "icon": child.icon,
                        "description": child.description,
                        "url": child.url,
                        "order": child.model_order
                    }
                    children.append(child_dict)
                data = {
                    "level": value.model_level,
                    "icon": value.icon,
                    "description": value.description,
                    "url": value.url,
                    "order": value.model_order,
                    "children": children
                }
                content.append(data)
            return JsonResponse(content, safe=False)
        except Exception as e:
            return server_error(message="用户数据不存在，请重试")


# 退出
class LogoutHandler(View):
    def post(self, request):
        response = ok()
        # 清除用户的token值
        response.set_cookie('token', '')
        response.set_cookie('session_id', '')
        # 将redis中存储的token值清除
        # redis_store.delete('token:%s' % username)
        return response


# 处理字典的视图集
class TDictionaryViewSet(viewsets.ModelViewSet):
    serializer_class = TDictionarySerializer  # 指定序列化类
    queryset = TDictionary.objects.all().order_by('id')  # 获取到查询集

    def list(self, request, *args, **kwargs):
        search_value = request.query_params.get('search_value', '')
        search_key = request.query_params.get('search_key', '')
        # 这个是将搜索和展示混合在一起
        queryset = TDictionary.objects.filter(dic_key__icontains=search_key, dic_value__icontains=search_value)
        page = self.paginate_queryset(queryset)  # 使用分页器函数
        if page is not None:
            # get_serializer 这个使用序列化类将对象序列化
            serializer = self.get_serializer(page, many=True)
            # get_paginated_response 使用带有分页功能的response
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 处理lookup管理视图集
class TLookupGroupViewSet(viewsets.ModelViewSet):
    serializer_class = TLookupGroupSerializer
    queryset = TLookupGroup.objects.all().order_by('id')
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('id',)

    def create(self, request, *args, **kwargs):
        id = request.POST.get('id', None)
        group_code = request.POST.get('group_code', None)
        group_name = request.POST.get('group_name', None)
        state = request.POST.get('state', None)
        parent_group_code = request.POST.get('parent_group_code', None)
        data = {
            'group_code': group_code,
            'group_name': group_name,
            'state': state,
            'parent_group_code': parent_group_code
        }
        # 这个是更新的代码
        if id:
            instance = TLookupGroup.objects.get(id=id)
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        # 这个是创建的代码
        serializer = self.get_serializer(data=data)  # 将要存储的字段序列化
        serializer.is_valid(raise_exception=True)  # 验证序列化字段是否满足要求
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 处理系统白名单视图集
class WhiteBlackListViewSet(viewsets.ModelViewSet):
    serializer_class = WhiteBlackListSerializer
    queryset = WhiteBlackList.objects.all().order_by('id')
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('role_type',)

    def list(self, request, *args, **kwargs):
        key = request.query_params.get('key', '')
        role_type = request.query_params.get('role_type', '')
        # 这个是将搜索和普通查询混合在一起
        queryset = WhiteBlackList.objects.filter(user_name__icontains=key, role_type=role_type)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # 这个对应的是删除多个对象
        if self.kwargs[self.lookup_field] == 'aa':
            id_list = request.POST.get('ids', '').split(',')
            WhiteBlackList.objects.filter(id__in=id_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # 这个是默认的删除某一个
        return super(WhiteBlackListViewSet, self).destroy(request, *args, **kwargs)


# 日志管理视图集
class SysLogViewSet(viewsets.ModelViewSet):
    serializer_class = SysLogSerializer
    queryset = SysLog.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        log_user = request.GET.get('logUser', None)
        create_time = request.GET.get('createTime', None)
        end_time = request.GET.get('endTime', None)
        # 这个对应的时常规的查询
        if log_user is None or create_time is None or end_time is None:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            # 这个对应的时搜索
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") if end_time else datetime.datetime.now()
            start_time = datetime.datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S") if create_time else datetime.datetime.strptime("1971-01-01 18:55:23", "%Y-%m-%d %H:%M:%S")
            queryset = SysLog.objects.filter(log_user__icontains=log_user, create_time__gt=start_time, create_time__lt=end_time)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # 这个对应的时删除多个
        if self.kwargs[self.lookup_field] == 'aa':
            id_list = request.POST.get('logIds', '').split(',')
            SysLog.objects.filter(id__in=id_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # 这个对应的是删除所有
        elif self.kwargs[self.lookup_field] == 'all':
            SysLog.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_204_NO_CONTENT)


# 菜单管理视图集
class SysPermissionViewSet(viewsets.ModelViewSet):
    serializer_class = SysPermissionSerializer
    queryset = SysPermission.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        # 这个是查询所有的权限
        if request.query_params.get('all') == 'all':
            queryset = SysPermission.objects.all()
        else:
            # 这个是将搜索和查询混合在一起
            key = request.query_params.get('key', '')
            queryset = SysPermission.objects.filter(description__icontains=key)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 角色管理视图集
class SysRoleViewSet(viewsets.ModelViewSet):
    serializer_class = SysRoleSerializer
    queryset = SysRole.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        if request.query_params.get('all') == 'all':
            queryset = SysRole.objects.all()
        else:
            key = request.query_params.get('key', '')
            role_id = request.query_params.get('roleId', None)
            if role_id is not None:
                pers = SysRolePermission.objects.filter(role_id=role_id)
                str = ','.join(["%s" % per.pers_id for per in pers])
                return Response(str)
            # 负责查询和信息展示
            queryset = SysRole.objects.filter(role_name__icontains=key)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        ids = request.POST.getlist('id', [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        querysetlist = []
        # 负责创建外键元素
        for id in ids:
            querysetlist.append(SysRolePermission(role_id=serializer.data['id'], pers_id=id))
        SysRolePermission.objects.bulk_create(querysetlist)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        SysRolePermission.objects.filter(role_id=instance.id).delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        ids = request.POST.getlist('id', [])
        instance = self.get_object()
        querysetlist = []
        for id in ids:
            querysetlist.append(SysRolePermission(role_id=instance.id, pers_id=id))
        SysRolePermission.objects.filter(role_id=instance.id).delete()
        SysRolePermission.objects.bulk_create(querysetlist)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


# 用户管理视图集
class SysUserViewSet(viewsets.ModelViewSet):
    serializer_class = SysUserSerializer
    queryset = SysUser.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        keyWord = request.query_params.get('keyWord', '')
        if request.query_params.get('role') == 'role':
            queryset = SysUserRole.objects.filter(user_id=request.query_params.get('id', None))
            context = []
            for query in queryset:
                context.append({
                    "id": query.id,
                    "role_id": query.role_id,
                    "user_id": query.user_id
                })
            return JsonResponse(context, safe=False)
        queryset = SysUser.objects.filter(user_name__icontains=keyWord)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user_name = request.POST.get("user_name", None)
        nick_name = request.POST.get("nick_name", None)
        password = request.POST.get("password", None)
        repassword = request.POST.get("repassword", None)
        role_ids = request.POST.get("role_id", '').split(',')
        if len(password) < 6 or password != repassword:
            return Response("输入密码有误，请重试")
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        password = hl.hexdigest()
        data = {
            "user_name": user_name,
            "nick_name": nick_name,
            "password": password
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        querysetlist = []
        for id in role_ids:
            querysetlist.append(SysUserRole(user_id=serializer.data['id'], role_id=id))
        SysUserRole.objects.bulk_create(querysetlist)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        SysUserRole.objects.filter(user_id=instance.id).delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        user_name = request.POST.get("user_name", None)
        nick_name = request.POST.get("nick_name", None)
        password = request.POST.get("password", None)
        repassword = request.POST.get("repassword", None)
        if len(password) < 6 or password != repassword:
            return Response("输入密码有误，请重试")
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        password = hl.hexdigest()
        data = {
            "user_name": user_name,
            "nick_name": nick_name,
            "password": password
        }
        partial = kwargs.pop('partial', False)
        ids = request.POST.get('roleId', '').split(',')
        instance = self.get_object()
        querysetlist = []
        for id in ids:
            querysetlist.append(SysUserRole(user_id=instance.id, role_id=id))
        SysUserRole.objects.filter(user_id=instance.id).delete()
        SysUserRole.objects.bulk_create(querysetlist)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
