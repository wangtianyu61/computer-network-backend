from django.shortcuts import render
from user.models import *
from django import http
from django.views import View
import json, requests
from django.db.models import Max
from django.db import transaction
from django.db import IntegrityError
from django.db.models import Sum, Count, Max, Min, Avg
from user.param import *
from django.http.response import *
import datetime


# def new_order_book(request):
#     postage = POSTAGE
#     print(request.body)
#     data = eval(str(request.body,encoding='utf-8'))
#     print(data)
#     customer_id = data['customer_id'] # customer id
#     order_info = data['order_detail']
#     result = {'success':1, 'message':''}
#     for bill in order_info: # 判断是否库存足够
#         entry_id = bill["entry_id"]
#         order_amount = bill["order_number"]
#         book = Entry.objects.get(entry_id=entry_id)
#         try:
#             inventory = book.customer_inventory
#         except:
#             result['success'] = 0
#         if int(inventory) < int(order_amount):
#             result['success'] = 0
#             result['message'] = "Books not enough"
#         if result['success'] == 0: break
#     if result['success'] == 1:
#         # Create OrderInfo
#         new_order = OrderInfo()
#         result['postage'] = len(order_info) * bill_postage
#         new_order.postageFee = result['postage']
#         new_order.customer_id = customer_id
#         new_order.order_time = datetime.datetime.now()
#         new_order.paymentType = 0
#         new_order.serial = -1
#         new_order.save()
#         print(new_order.order_id)
#         result['order_id'] = new_order.order_id
#         new_order.serial = new_order.order_id + 100
#         new_order.save()
#         # Add Order Detail

#     else:
#         return http.JsonResponse(result,safe=False,json_dumps_params={'ensure_ascii':False})
    

def order_book(request):
    bill_postage = POSTAGE
    print(request.body)
    data = json.loads(request.body, strict = False)
    print(data)
    customer_id = data['customer_id'] # customer id
    order_info = data['order_detail']

    result = {'success':1,'order_id':-1,'postage':-1}
    for bill in order_info: # 判断是否库存足够
        entry_id = bill["entry_id"]
        order_amount = bill["inventory"]
        book = Entry.objects.get(entry_id=entry_id)
        try:
            inventory = book.customer_inventory
        except:
            result['success'] = 0
        if int(inventory) < int(order_amount): result['success'] = 0
        if result['success'] == 0: break
    if result['success'] == 1: # Create OrderInfo
        new_order = OrderInfo()
        result['postage'] = len(order_info) * bill_postage
        new_order.postageFee = result['postage']
        new_order.customer_id = customer_id
        new_order.order_time = datetime.datetime.now()
        new_order.paymentType = 0
        new_order.serial = -1
        new_order.save()
        print(new_order.order_id)
        result['order_id'] = new_order.order_id
        new_order.serial = new_order.order_id + 100
    #print(result)
    return http.JsonResponse(result,safe=False,json_dumps_params={'ensure_ascii':False})

def confirm_order_book(request):
    print('Confirm Order')
    postage = POSTAGE
    print(request.body)
    data = json.loads(request.body, strict = False)
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
        receive_type = data['ReceiveType']
        # Update OrderInfo
        order.paymentType = payment_type
        order.save()
        # Create OrderDetail
        for book in order_info:
            entry_id = book["entry_id"]
            amount = book["inventory"]
            # Update Entry
            entry = Entry.objects.get(entry_id=entry_id)
            entry.customer_inventory -= amount
            entry.save()
            # Create OrderDetail
            print(order)
            print(type(order))
            order_detail = OrderDetail()
            order_detail.order_id = order
            order_detail.entry_id = entry_id
            order_detail.number = amount
            order_detail.seller_id = entry.seller_id
            order_detail.deliver_time = datetime.datetime.now()
            order_detail.postageFee = POSTAGE
            order_detail.status = 0
            order_detail.receiveType = UserAccountType.objects.filter(user_id = entry.seller_id)[0].payment_type
            order_detail.save()
    return http.HttpResponse('菊神真帅')

#see the order for the seller
def order_of(request, pk):
    select_orders = OrderDetail.objects.filter(seller_id = pk)
    query_res_list = list(select_orders.values())
    # need to add the entry name if possible 
    print(query_res_list)
    for query_res_elem in query_res_list:
        # add the book name
        query_res_elem["book_name"] = Entry.objects.get(entry_id = query_res_elem["entry_id"]).name 
        #find and add the corresponding customer address
        customerid = OrderInfo.objects.get(order_id = query_res_elem["order_id_id"]).customer_id
        query_res_elem["customer_address"] = UserInfo.objects.get(user_id = customerid).address
    res = JsonResponse(query_res_list, safe = False)
    return res    

## seller pack the book
def pack_book_update(request):
    data = eval(str(request.body,encoding='utf-8'))
    print(data)
    pack_info = {"success":1, "message":""}
    try:
        order_id = data['order_id']
        entry_id = data['entry_id']
        order_info = OrderInfo.objects.get(order_id = order_id)          
        order_detail = OrderDetail.objects.get(order_id = order_info, entry_id = entry_id)
        order_detail.status = 1
        order_detail.save()
    except Exception as e:
        pack_info['message'] = str(e)
        pack_info["success"] = 0 
    return http.JsonResponse(pack_info)


def receive_book_confirm(request):
    print(request.body)
    data = eval(str(request.body,encoding='utf-8'))
    print(data)
    customer_id = data['customer_id']
    order_id = data['order_id']
    result = {'success':0,'message':''}
    try:
        order_overall = OrderInfo.objects.get(order_id=order_id)
        order_overall.status = 2
        order_overall.save()

        result['success'] = 1
    except Exception as e:
        result['message'] = str(e)
    return http.JsonResponse(result,safe=False,json_dumps_params={'ensure_ascii':False})


def test_view_order_info(request):
    books = Entry.objects.filter()
    for book in books:
        print(book.entry_id)
        print(book.customer_inventory)
        # book.customer_inventory = 100
        # book.save()
        print('*'*20)

    # entry = Entry.objects.get(entry_id=1)
    # entry.customer_inventory += 100
    # print(entry.customer_inventory)
    return http.HttpResponse()