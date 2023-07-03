#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from rest_framework import viewsets
from .models import TCustomerUser, TGroup
from .serializers import TCustomerUserSerializer, TGroupSerializer
from rest_framework.response import Response
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from apps.pay.models import TPayInfo
from rest_framework import status


# 会员列表视图集
class TCustomerUserViewSet(viewsets.ModelViewSet):
    serializer_class = TCustomerUserSerializer
    queryset = TCustomerUser.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        group_id = request.GET.get("groupId", None)
        user_account = request.GET.get("userAccount", None)
        if group_id is not None or user_account is not None:
            if group_id is not "":
                queryset = TCustomerUser.objects.filter(user_account__icontains=user_account, group_id=group_id)
            else:
                queryset = TCustomerUser.objects.filter(user_account__icontains=user_account)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if self.kwargs[self.lookup_field] == 'all':
            id_list = request.POST.get('ids', '').split(',')
            TCustomerUser.objects.filter(id__in=id_list).delete()
        else:
            instance = self.get_object()
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# 会员分级视图集
class TGroupViewSet(viewsets.ModelViewSet):
    serializer_class = TGroupSerializer
    queryset = TGroup.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        if request.GET.get('all', None) == 'all':
            queryset = TGroup.objects.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        page = request.GET.get('page', '1')
        limit = request.GET.get('limit', '10')
        try:
            page_int = int(page)
            limit_int = int(limit)
            values = TGroup.objects.all()
            p = Paginator(values, limit)
            data_dict = []
            for value in p.page(page):
                value_dict = {
                    "id": value.id,
                    "name": value.name
                }
                if value.str_values:
                    value.str_values = json.loads(value.str_values)
                    for key, dic in value.str_values.items():
                        value_dict[key] = dic.split('&')[1]
                data_dict.append(value_dict)
            return JsonResponse({'count': p.count, 'results': data_dict})
        except Exception as e:
            return JsonResponse({'code': 2, 'msg': '查找信息失败'})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        str_list = request.POST.get('strValues', '').split(',')
        str_values = {}
        for str_value in str_list:
            if str_value:
                str_values[str_value.split('&')[0]] = str_value
        if str_values:
            str_values = json.dumps(str_values)
        else:
            str_values = None
        data = {
            "str_values": str_values
        }
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
