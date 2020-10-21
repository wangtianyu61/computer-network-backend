from django.shortcuts import render
from user.models import *
from django import http
from django.views import View
import json, requests
from django.db.models import Max
from django.db import transaction
from django.db import IntegrityError
from django.db.models import Sum, Count, Max, Min, Avg



def order_book(request):
    bill_postage = 3
    print(request.body)
    data = eval(str(request.body,encoding='utf-8'))
    print(data)
    customer_id = data['customer_id'] # customer id
    order_info = data['order_detail']

    result = {'success':1,'order_id':-1,'postage':-1}
    for bill in order_info:
        entry_id = bill[0]
        order_amount = bill[1]
        book = Entry.objects.get(entry_id=entry_id)
        try:
            inventory = book.customer_inventory
        except:
            result['success'] = 0
        if inventory < order_amount: result['success'] = 0
        if result['success'] == 0: break
    if result['success'] == 1:
        new_order = OrderInfo()
        new_order.save()
        result['order_id'] = new_order.order_id
        result['postage'] = len(order_info) * bill_postage
    return JsonResponse(result,safe=False,json_dumps_params={'ensure_ascii':False})

def order_book_confirm(request):
    pass