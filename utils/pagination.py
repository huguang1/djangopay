#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    limit = 10
    page_size_query_param = 'limit'
    page_query_param = "page"
    max_page_size = 100