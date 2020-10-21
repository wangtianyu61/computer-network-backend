from django.shortcuts import render
from user.models import *
from django import http
from django.views import View
import json, requests
from django.db.models import Max
from django.db import transaction
from django.db import IntegrityError
from django.db.models import Sum, Count, Max, Min, Avg

POSTAGE = 3

def order_book(request):
    bill_postage = POSTAGE
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
        result['order_id'] = new_order.order_id
        result['postage'] = len(order_info) * bill_postage
        new_order.postageFee = result['postage']
        new_order.customer_id = customer_id
        new_order.order_time = datetime.datetime.now()
        new_order.paymentType = 0
        new_order.save()
    return JsonResponse(result,safe=False,json_dumps_params={'ensure_ascii':False})

def order_book_confirm(request):
    postage = POSTAGE
    print(request.body)
    data = eval(str(request.body,encoding='utf-8'))
    print(data)

    action = data['action']
    order_id = data['order_id']
    if action == 0: # Order canceled
        try:
            order = OrderInfo.objects.get(order_id = order_id)
            order.delete()
        except:
            pass
    else: # Order confirmed
        order = OrderInfo.objects.get(order_id = order_id)
        customer_id = data['customer_id']
        payment_type = data['PaymentType']
        order_info = data['order_detail']
        # Update OrderInfo
        order.paymentType = payment_type
        # Create OrderDetail
        for book in order_info:
            entry_id = book[0]
            amount = book[1]
            # Update Entry
            entry = Entry.objects.get(entry_id=entry_id)
            entry.customer_inventory -= amount
            entry.save()
            # Create OrderDetail
            order_detail = OrderDetail()
            order_detail.order_id = order_id
            order_detail.entry_id = entry_id
            order_detail.number = amount
            order_detail.seller_id = entry.seller_id
            order_detail.deliver_time = datetime.datetime.now()
            order_detail.postageFee = POSTAGE
            order_detail.status = 0
            order_detail.save()
    return http.HttpResponse()

def receive_book_confirm(request):
    pass