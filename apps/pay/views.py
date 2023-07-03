#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from django.http import JsonResponse
from rest_framework import viewsets
from .models import TPayCode, TLookupItem, TPayApi, TPayInfo
from .serializers import TPayCodeSerializer, TLookupItemSerializer, TPayApiSerializer, TPayInfoSerializer
from rest_framework import filters
from django_filters import rest_framework
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
import base64
from apps.cfg.models import TGroup
import json


# 支付二维码视图集
class TPayCodeViewSet(viewsets.ModelViewSet):
    serializer_class = TPayCodeSerializer
    queryset = TPayCode.objects.all().order_by('id')
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('pay_code', )

    def create(self, request, *args, **kwargs):
        pay_type = request.POST.get('payType', None)
        comment = request.POST.get('comment', None)
        files = request.FILES
        comment = files['file'].name
        body = files['file'].read()
        body = "data:image/png;base64," + str(base64.b64encode(body), encoding='utf-8')
        data = {
            "code": body,
            "comment": comment,
            "pay_code": pay_type,
            "status": 0
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 支付类型视图集
class TLookupItemViewSet(viewsets.ModelViewSet):
    serializer_class = TLookupItemSerializer
    queryset = TLookupItem.objects.all().order_by('id')
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('group_code', 'id', 'state')

    def list(self, request, *args, **kwargs):
        if request.GET.get('all') == 'all':
            group_code = request.GET.get('group_code', '')
            state = request.GET.get('state', '')
            queryset = TLookupItem.objects.filter(group_code=group_code, state=state)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        attribute_1 = request.POST.get('attribute_1', None)
        attribute_2 = request.POST.get('attribute_2', None)
        attribute_3 = request.POST.get('attribute_3', None)
        attribute_4 = request.POST.get('attribute_4', None)
        group_code = request.POST.get('groupCode', None)
        id = request.POST.get('id', None)
        item_code = request.POST.get('item_code', None)
        item_name = request.POST.get('item_name', None)
        sort = request.POST.get('sort', None)
        state = request.POST.get('state', None)
        data = {
            "attribute_1": attribute_1,
            "attribute_2": attribute_2,
            "attribute_3": attribute_3,
            "attribute_4": attribute_4,
            "group_code": group_code,
            "item_code": item_code,
            "item_name": item_name,
            "sort": sort,
            "state": state
        }
        if id:
            instance = TLookupItem.objects.get(id=id)
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 支付平台视图集
class TPayApiViewSet(viewsets.ModelViewSet):
    serializer_class = TPayApiSerializer
    queryset = TPayApi.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        if request.GET.get('one') == 'one':
            queryset = TPayApi.objects.filter(id=request.GET.get('id'))
        elif request.GET.get('all') == 'all':
            queryset = TPayApi.objects.all()
        else:
            payment_code = request.GET.get('paymentCode', '')
            queryset = TPayApi.objects.filter(Q(payment_code__icontains=payment_code) | Q(payment_name__icontains=payment_code))
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        api_key = request.POST.get('api_key', None)
        attribute_1 = request.POST.get('attribute_1', None)
        attribute_2 = request.POST.get('attribute_2', None)
        attribute_3 = request.POST.get('attribute_3', None)
        attribute_4 = request.POST.get('attribute_4', None)
        attribute_5 = request.POST.get('attribute_5', None)
        callback_url = request.POST.get('callback_url', None)
        http_type = request.POST.get('http_type', None)
        http_url = request.POST.get('http_url', None)
        id = request.POST.get('id', '')
        memberid = request.POST.get('memberid', None)
        notify_type = request.POST.get('notify_type', None)
        notify_url = request.POST.get('notify_url', None)
        param_format = request.POST.get('param_format', None)
        payment_code = request.POST.get('payment_code', None)
        payment_name = request.POST.get('payment_name', None)
        query_url = request.POST.get('query_url', None)
        remark = request.POST.get('remark', None)
        sign_format = request.POST.get('sign_format', None)
        sign_type = request.POST.get('sign_type', None)
        state = request.POST.get('state', None)
        verify_format = request.POST.get('verify_format', None)
        data = {
            "api_key": api_key,
            "attribute_1": attribute_1,
            "attribute_2": attribute_2,
            "attribute_3": attribute_3,
            "attribute_4": attribute_4,
            "attribute_5": attribute_5,
            "callback_url": callback_url,
            "http_type": http_type,
            "http_url": http_url,
            "memberid": memberid,
            "notify_type": notify_type,
            "notify_url": notify_url,
            "param_format": param_format,
            "payment_code": payment_code,
            "payment_name": payment_name,
            "query_url": query_url,
            "remark": remark,
            "sign_format": sign_format,
            "sign_type": sign_type,
            "state": state,
            "verify_format": verify_format
        }
        if id:
            instance = TPayApi.objects.get(id=id)
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 支付通道视图集
class TPayInfoViewSet(viewsets.ModelViewSet):
    serializer_class = TPayInfoSerializer
    queryset = TPayInfo.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        item_code = request.GET.get('itemCode', None)
        payment_code = request.GET.get('paymentCode', '')
        id = request.GET.get('id', None)
        payment_code = request.GET.get("payment_code", None)
        if request.GET.get("all", None) == "all":
            queryset = TPayInfo.objects.all()
            serializer = self.get_serializer(queryset, many=True)
            value = TGroup.objects.get(id=request.GET.get("id", ""))
            value_dict = {
                "id": value.id,
                "name": value.name,
            }
            if value.str_values:
                value.str_values = json.loads(value.str_values)
                for key, dic in value.str_values.items():
                    value_dict[key] = dic
            data = {
                "availablePayInfo": serializer.data,
                "group": value_dict
            }
            return JsonResponse({"data": data, "code": 0})
        elif id:
            queryset = TPayInfo.objects.filter(id=id)
        elif payment_code:
            queryset = TPayInfo.objects.filter(payment_code=payment_code)
        else:
            if item_code is None:
                queryset = self.filter_queryset(self.get_queryset())
            else:
                queryset = TPayInfo.objects.filter(item_code__startswith=item_code).filter(Q(payment_code__icontains=payment_code) | Q(payment_name__icontains=payment_code))
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        bank_code = request.POST.get('bank_code', None)
        id = request.POST.get('id', '')
        item_code = request.POST.get('item_code', '')
        max_amount = request.POST.get('max_amount', None)
        max_switch = request.POST.get('max_switch', None)
        min_amount = request.POST.get('min_amount', None)
        min_switch = request.POST.get('min_switch', None)
        pay_code = request.POST.get('pay_code', None)
        payment_code = request.POST.get('payment_code', '')
        point_switch = request.POST.get('point_switch', None)
        rate = request.POST.get('rate', None)
        rate_type = request.POST.get('rate_type', None)
        state = request.POST.get('state', None)
        wangyinType = request.POST.get('wangyin_type', None)
        try:
            lookup = TLookupItem.objects.get(item_code=item_code)
            if lookup.attribute_1 == 'PC':
                pay_model = 1
            elif lookup.attribute_1 == 'WAP':
                pay_model = 2
            elif lookup.attribute_1 == '网银内部':
                pay_model = 3
            elif lookup.attribute_1 == '网银外部':
                pay_model = 4
            else:
                pay_model = 0
            item_name = lookup.item_name
            icon = lookup.attribute_4
            payapi = TPayApi.objects.get(payment_code=payment_code)
            payment_name = payapi.payment_name
            data = {
                "bank_code": bank_code,
                "item_code": item_code,
                "max_amount": max_amount,
                "max_switch": max_switch,
                "min_amount": min_amount,
                "min_switch": min_switch,
                "pay_code": pay_code,
                "payment_code": payment_code,
                "point_switch": point_switch,
                "rate": rate,
                "rate_type": rate_type,
                "state": state,
                "pay_model": pay_model,
                "item_name": item_name,
                "icon": icon,
                "payment_name": payment_name
            }
        except Exception as e:
            return JsonResponse({'code': 1, 'error': '输入有误请重试'})
        if id:
            instance = TPayInfo.objects.get(id=id)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
