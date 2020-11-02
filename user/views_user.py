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
    target_obj = UserInfo.objects.get(user_id = user_id)
    dict_obj = model_to_dict(target_obj)
    print(dict_obj)
    res = JsonResponse(dict_obj, safe = False)
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
  

def edit_user_info(request):
    data_dict = json.loads(str(request.body,encoding='utf-8'))
    user_id = data_dict['user_id']
    avatar = data_dict['avatar']
    real_name = data_dict['real_name']
    age = data_dict['age']
    sex = data_dict['sex']
    certificationType = data_dict['certificationType']
    certificationNumber = data_dict['certificationNumber']
    address = data_dict['address']
    username = data_dict['username']
    password = data_dict['password']
    telephone = data_dict['telephone']
    target_user = UserInfo.objects.get(user_id = user_id)
    target_user.avatar = avatar
    target_user.real_name = real_name
    target_user.age = age
    target_user.sex = sex
    target_user.certificationType = certificationType
    target_user.certificationNumber = certificationNumber
    target_user.address = address
    target_user.password = password
    target_user.telephone = telephone
    target_user.save()



