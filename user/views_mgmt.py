from django.shortcuts import render
from user.models import *
from django import http
from django.views import View
import json, requests
from django.db.models import Max
from django.db import transaction
from django.db import IntegrityError
from django.db.models import Sum, Count, Max, Min, Avg

@transaction.atomic
def user_register(request):
    #get the register data
    user_info = json.loads(request.body, strict = False)
    register_info = {"success":0, "message":"", "user_id":0}
    max_user_id = UserInfo.objects.all().aggregate(Max('user_id'))['user_id__max']
    save_tag = transaction.savepoint()
    ## check whether it is empty
    for user_key in user_info.keys():
        if len(user_info[user_key]) == 0:
            register_info["message"] = "The item " + user_key + " cannot be empty!"
            return http.JsonResponse(register_info)
    
    ## check logic
    ### phone
    if user_info["phone"].isdigit() == True and len(user_info["phone"])!=11:
        register_info["message"] = "It is not a valid phone number!"
        return http.JsonResponse(register_info)
    #### truncate with the phone number in db
    if len(UserInfo.objects.filter(phone = user_info["phone"])) == 1:
        register_info["message"] = "Phone truncated!"
    ### username
    if len(user_info["username"])>10:
        register_info["message"] = "Too long for a username!(The maximum length is 10)!"
        return http.JsonResponse(register_info)
    #### truncate with the username in db
    if len(UserInfo.objects.filter(username = user_info["username"])) == 1:
        register_info["message"] = "User name truncated!"
        return http.JsonResponse(register_info)

    ## add the user info
    try:
        with transaction.atomic():
            UserInfo.objects.create(**dict_data)
            ### add successfully
            register_info["success"] = 1
            register_info["user_id"] = max_user_id + 1
    except Exception as e:
        register_info["message"] = str(e)
        transaction.savepoint_rollback(save_tag)

    return http.JsonResponse(register_info)  

def user_login(request):
    #get the login data
    user_info = json.loads(request.body, strict = False)
    login_info = {"success":0, "username":"", "avatar":"","user_id":0}
    check_name = user_info["username_or_phone"]
    ## search by name
    if len(check_name) < 11:
        try:
            user_detail = Userinfo.objects.get(user_id = check_name, password = user_info["password"])
            login_info["success"] = 1
            login_info["username"] = user_detail.username
            login_info["avatar"] = user_detail.avatar
            login_info["user_id"] = user_detail.user_id
        ## not found
        except Exception as e:
            pass
    ## search by phone number
    else:
        try:
            user_detail = Userinfo.objects.get(phone = check_name, password = user_info["password"])
            login_info["success"] = 1
            login_info["username"] = user_detail.username
            login_info["avatar"] = user_detail.avatar
            login_info["user_id"] = user_detail.user_id
        ## not found
        except Exception as e:
            pass
    return http.JsonResponse(login_info)
            
