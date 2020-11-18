from django.shortcuts import render
from user.models import *
from django import http
from django.views import View
import json, requests
from django.db.models import Max
from django.db import transaction
from django.db import IntegrityError
from django.db.models import Sum, Count, Max, Min, Avg
from django.forms.models import model_to_dict
from django.http.response import *
from datetime import datetime

def user_info(request):
    # tmp = str(request.body,encoding='utf-8')
    # print(tmp)
    data_dict = json.loads(str(request.body,encoding='utf-8'), strict = False)
    user_id = data_dict['user_id']
    try:
        target_obj = UserInfo.objects.get(user_id = user_id)
        dict_obj = model_to_dict(target_obj)
        #print(dict_obj)
        # add the transaction type given this user
        account_obj = UserAccountType.objects.filter(user_id = user_id)
        dict_obj['account'] = []
        for account_detail in account_obj:
            dict_obj['account'].append({"payment_type":account_detail.payment_type,
                                        "account_id":account_detail.account_id,
                                        "priority":account_detail.priority})
        res = http.JsonResponse(dict_obj, safe = False)
    except Exception as e:
        print(e)
        res = http.JsonResponse({}, safe = False)
    return res

def user_order_all(request):
    # tmp = str(request.body,encoding='utf-8')
    # print(tmp)
    data_dict = json.loads(str(request.body,encoding='utf-8'))
    user_id = data_dict['user_id']
    query_res_list = list(OrderInfo.objects.filter(customer_id = user_id).values())
    #change the book name
    for query_res_elem in query_res_list:
        query_res_elem["order_time"] = query_res_elem["order_time"].strftime('%Y%m%d %H:%M:%S')
        #the sum of prices
        sum_price = 0
        orderinfo = OrderInfo.objects.get(order_id = query_res_elem["order_id"])
        order_detail = OrderDetail.objects.filter(order_id = orderinfo)
        for each_order_entry in order_detail:
            order_entry = Entry.objects.get(entry_id = each_order_entry.entry_id)
            sum_price += order_entry.price*each_order_entry.number
        query_res_elem["total_price"] = sum_price
    
    res = http.JsonResponse(query_res_list, safe = False)
    print("the current order",query_res_list)
    return res        

def user_order_detail(request, pk):
    order_user_id = OrderInfo.objects.get(order_id = pk)
    query_res_list = list(OrderDetail.objects.filter(order_id = order_user_id).values())
    # need to add the entry name if possible 
    sum_price = 0
    for query_res_elem in query_res_list:
        order_entry = Entry.objects.get(entry_id = query_res_elem["entry_id"])
        query_res_elem['total_price'] = int(query_res_elem["number"])*order_entry.price
        query_res_elem["entry_name"] = Entry.objects.get(entry_id = query_res_elem["entry_id"]).name 

    print('order info', query_res_list)
    res = http.JsonResponse(query_res_list, safe = False)
    return res        

def user_order_deliver(request):
    data_dict = json.loads(str(request.body,encoding='utf-8'))
    user_id = data_dict['user_id']
    query_res_list = list(OrderInfo.objects.filter(status = 0).values())
        #change the book name
    for query_res_elem in query_res_list:
        query_res_elem["order_time"] = query_res_elem["order_time"].strftime('%Y%m%d %H:%M:%S')
        #the sum of prices
        sum_price = 0
        orderinfo = OrderInfo.objects.get(order_id = query_res_elem["order_id"])
        order_detail = OrderDetail.objects.filter(order_id = orderinfo)
        for each_order_entry in order_detail:
            order_entry = Entry.objects.get(entry_id = each_order_entry.entry_id)
            sum_price += order_entry.price*each_order_entry.number
        query_res_elem["total_price"] = sum_price
    res = http.JsonResponse(query_res_list, safe = False)
    return res        

def user_order_transport(request):
    data_dict = json.loads(str(request.body,encoding='utf-8'))
    user_id = data_dict['user_id']
    query_res_list = list(OrderInfo.objects.filter(status = 1).values())
    #change the book name
    for query_res_elem in query_res_list:
        query_res_elem["order_time"] = query_res_elem["order_time"].strftime('%Y%m%d %H:%M:%S')
        #the sum of prices
        sum_price = 0
        orderinfo = OrderInfo.objects.get(order_id = query_res_elem["order_id"])
        order_detail = OrderDetail.objects.filter(order_id = orderinfo)
        for each_order_entry in order_detail:
            order_entry = Entry.objects.get(entry_id = each_order_entry.entry_id)
            sum_price += order_entry.price*each_order_entry.number
        query_res_elem["total_price"] = sum_price
    res = http.JsonResponse(query_res_list, safe = False)
    return res        

def user_order_finished(request):
    data_dict = json.loads(str(request.body,encoding='utf-8'))
    user_id = data_dict['user_id']
    query_res_list = list(OrderInfo.objects.filter(status = 2).values())
    #change the book name
    for query_res_elem in query_res_list:
        query_res_elem["order_time"] = query_res_elem["order_time"].strftime('%Y%m%d %H:%M:%S')
        #the sum of prices
        sum_price = 0
        orderinfo = OrderInfo.objects.get(order_id = query_res_elem["order_id"])
        order_detail = OrderDetail.objects.filter(order_id = orderinfo)
        for each_order_entry in order_detail:
            order_entry = Entry.objects.get(entry_id = each_order_entry.entry_id)
            sum_price += order_entry.price*each_order_entry.number
        query_res_elem["total_price"] = sum_price
    res = http.JsonResponse(query_res_list, safe = False)
    return res        
  
@transaction.atomic
def edit_user_info(request):
    data_dict = json.loads(str(request.body,encoding='utf-8'))
    user_id = data_dict['user_id']

    # print(data_dict)
    save_tag = transaction.savepoint()
    edit_info = {"success":1, "message":""}
    try:
        with transaction.atomic():
            #change the user basic info
            target_user = UserInfo.objects.filter(user_id = user_id)
            account_info = data_dict['account']
            del data_dict['account']

            target_user.update(**data_dict)
            #change the account info    
            ##delete the past
            old_account = UserAccountType.objects.filter(user_id = user_id).delete()
            ##add the new
            for account_detail in account_info:
                account_detail['user_id'] = target_user
                print(account_detail)
                user_account_info = UserAccountType.objects.create(serial_id = 2*len(UserAccountType.objects.all()) + 1,
                                                                    user_id = target_user[0], 
                                                                    payment_type = account_detail['payment_type'],
                                                                    account_id = account_detail['account_id'],
                                                                    priority = account_detail['priority'])
                                                                    
                
        #did not change correctly and need to rollback
    except Exception as e:
        edit_info['success'] = 0
        edit_info['message'] = str(e)
    return http.JsonResponse(edit_info)

def entry_comment(request):
    comment_info = json.loads(request.body, strict = False)
    add_info = {"success":1, "message":""} 
    try:
        entry_info = Entry.objects.get(entry_id = comment_info["entry_id"])
        entry_comment_len = len(EntryComment.objects.filter(entry_id = comment_info["entry_id"]))
        EntryComment.objects.create(entry_id = entry_info, entry_comment_id = entry_current_comment_len + 1, 
                                comment_time = datetime.now())
    except Exception as e:
        add_info["message"] = str(e)
        add_info["success"] = 0
    return http.JsonResponse(add_info, safe = False)
                                
def entry_feedback(request):
    comment_info = json.loads(request.body, strict = False)
    add_info = {"success":1, "message":""}
    try:
        entry_comment = EntryComment.objects.get(comment_info["entry_id"], comment_info["entry_comment_id"])
        entry_comment.entry_feedback = comment_info["feedback"]
        entry_comment.feedback_time = datetime.now() 
    except Exception as e:
        add_info["message"] = str(e)
        add_info["success"] = 0
    return http.JsonResponse(add_info, safe = False)

