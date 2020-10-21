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
    print(request.body)
    data = eval(str(request.body,encoding='utf-8'))
    print(data)
    customer_id = data['customer_id'] # customer id
    order_info = data['order_detail']
    entry_id = order_info[0] # entry id
    order_number = order_info[1] # order amount

    book = Entry.objects.get(entry_id=entry_id)
    
    pass