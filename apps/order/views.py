#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/6/11
from rest_framework import viewsets
from .models import TOrderHis, TOrder
from .serializers import TOrderHisSerializer, TOrderSerializer
from rest_framework.response import Response
from django.http import JsonResponse
import datetime
from apps.pay.models import TPayInfo
from django.db.models import Q
from django.db.models import Sum, Count
from django.core.paginator import Paginator


# 历史订单列表视图集
class TOrderHisViewSet(viewsets.ModelViewSet):
    serializer_class = TOrderHisSerializer
    queryset = TOrderHis.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        page = request.GET.get('page', '1')
        limit = request.GET.get('limit', '10')
        start_time = request.GET.get('startTime', '')
        end_time = request.GET.get('endTime', '')
        order_state = request.GET.get('orderState', '')
        key = request.GET.get('key', '')  # 用户名，订单编号，操作人
        if order_state == '':
            order_state = 30
        page_int = int(page)
        limit_int = int(limit)
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") if end_time else datetime.datetime.now()
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") if start_time else datetime.datetime.strptime("1971-01-01 18:55:23", "%Y-%m-%d %H:%M:%S")
        queryset = TOrderHis.objects.filter(Q(user_account__icontains=key) | Q(order_id__icontains=key) | Q(update_user__icontains=key)).filter(order_state=order_state, order_time__gt=start_time, order_time__lt=end_time)
        sums = TOrderHis.objects.filter(Q(user_account__icontains=key) | Q(order_id__icontains=key) | Q(update_user__icontains=key)).filter(order_state=order_state, order_time__gt=start_time, order_time__lt=end_time).aggregate(order_amount=Sum('order_amount'), rate_amount=Sum('rate_amount'))
        data_list = []
        responseData = {
            "allMoney": sums['order_amount'] if sums['order_amount'] else 0,
            "allPoundage": sums['rate_amount'] if sums['rate_amount'] else 0
        }
        p = Paginator(queryset, limit_int)
        count = p.count
        items = p.page(page_int)
        for item in items:
            data_dict = item.to_full_dict()
            # data_dict["payName"] = item.item_name
            # data_dict["paymentName"] = item.payment_name
            data_list.append(data_dict)
        return JsonResponse({"data": data_list, "count": count, "responseData": responseData})


# 待处理订单表视图集
class TOrderViewSet(viewsets.ModelViewSet):
    serializer_class = TOrderSerializer
    queryset = TOrder.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        page = request.GET.get('page', '1')
        limit = request.GET.get('limit', '10')
        order_state = request.GET.get('orderState', '')
        key = request.GET.get('key', '')  # 用户名，订单编号，操作人
        page_int = int(page)
        limit_int = int(limit)
        queryset = TOrder.objects.filter(Q(user_account__icontains=key) | Q(order_id__icontains=key) | Q(update_user__icontains=key)).filter(order_state=order_state, state=10)
        sums = TOrder.objects.filter(Q(user_account__icontains=key) | Q(order_id__icontains=key) | Q(update_user__icontains=key)).filter(order_state=order_state, state=10).aggregate(order_amount=Sum('order_amount'), rate_amount=Sum('rate_amount'))
        p = Paginator(queryset, limit_int)
        items = p.page(page_int)
        count = p.count
        data_list = []
        responseData = {
            "allMoney": sums['order_amount'] if sums['order_amount'] else 0,
            "allPoundage": sums['rate_amount'] if sums['rate_amount'] else 0
        }
        for item in items:
            data_dict = item.to_full_dict()
            # data_dict["payName"] = item.item_name
            # data_dict["paymentName"] = item.payment_name
            data_list.append(data_dict)
        return JsonResponse({"data": data_list, "count": count, "responseData": responseData})







        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = {
            "update_time": datetime.datetime.now(),
            "state": 20,
            "lock_id": "admin"
        }
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


