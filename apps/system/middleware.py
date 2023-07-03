#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from django.utils.deprecation import MiddlewareMixin
from utils.restful import ok, params_error, forbidden
from django.core.cache import cache


class SystemMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 当前url
        current_url = request.path_info
        # 请求方式
        current_method = request.method
        # 登陆页面等部分页面需要跳过
        if current_url == '/config/getlogin/token' or current_url == '/config/cache' or current_url == '/check/login' or current_url == '':
            return None
        #获取到用户名
        session_id = request.COOKIES.get('session_id')
        username = cache.get('sess_%s' % session_id)
        if username:
            request.username = username
        else:
            return params_error(message='用户名过期')

        # if current_method == 'POST':
        #     header_token = request.META.get("X-Csrf-Token")
        #     cookie_token = request.COOKIES.get('token')
        #     if cookie_token != header_token:
        #         return forbidden(message='token值已过期')
