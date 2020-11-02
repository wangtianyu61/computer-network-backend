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

def user_info(request):
    data_dict = json.loads(str(request.body,encoding='utf-8'))
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
        res = JsonResponse(dict_obj, safe = False)
    except Exception as e:
        print(e)
        res = JsonResponse({}, safe = False)
    return res

def user_order_all(request):
    data_dict = json.loads(str(request.body,encoding='utf-8'))
    user_id = data_dict['user_id']
    query_res_list = list(OrderInfo.objects.filter(user_id = user_id).values())
    res = JsonResponse(query_res_list, safe = False)
    return res        

def user_order_deliver(request):
    data_dict = json.loads(str(request.body,encoding='utf-8'))
    user_id = data_dict['user_id']
    query_res_list = list(OrderInfo.objects.filter(status = 0).values())
    res = JsonResponse(query_res_list, safe = False)
    return res        

def user_order_transport(request):
    data_dict = json.loads(str(request.body,encoding='utf-8'))
    user_id = data_dict['user_id']
    query_res_list = list(OrderInfo.objects.filter(status = 1).values())
    res = JsonResponse(query_res_list, safe = False)
    return res        

def user_order_finished(request):
    data_dict = json.loads(str(request.body,encoding='utf-8'))
    user_id = data_dict['user_id']
    query_res_list = list(OrderInfo.objects.filter(status = 2).values())
    res = JsonResponse(query_res_list, safe = False)
    return res        
  
@transaction.atomic
def edit_user_info(request):
    data_dict = json.loads(str(request.body,encoding='utf-8'))
    user_id = data_dict['user_id']

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
                user_account_info = UserAccountType.objects.create(serial_id = len(UserAccountType.objects.all()) + 1,
                                                                    user_id = target_user[0], 
                                                                    payment_type = account_detail['payment_type'],
                                                                    account_id = account_detail['account_id'],
                                                                    priority = account_detail['priority'])
                                                                    
                
        #did not change correctly and need to rollback
    except Exception as e:
        edit_info['success'] = 0
        edit_info['message'] = str(e)
    return http.JsonResponse(edit_info)


