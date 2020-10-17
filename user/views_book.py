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

#the sell gets the book of his own.
def book_of(request, pk):
    select_entries = Entry.objects.filter(seller_id = pk)
    all_entry_info = []
    for select_entry in select_entries:
        if select_entry.seller_inventory >= 0:
            entry_info = {"entry_id":select_entry.entry_id,
                        "name":select_entry.name,
                        "author":select_entry.author,
                        "category":select_entry.category,
                        "price":select_entry.price,
                        "original_price":select_entry.original_price,
                        "inventory":select_entry.seller_inventory}
            all_entry_info.append(entry_info)
    return http.JsonResponse({"book_info":all_entry_info}, strict = False)

# add the book entry for the seller
@transaction.atomic
def add_book_entry(request):
    book_info = json.loads(request.body, strict = False)
    add_info = {"success":0, "message":""} 
    ## check the logic
    if book_info["original_price"] < 0:
        add_info["message"] = "The original price cannot be negative!"
        return http.HttpResponse(add_info)
    if book_info["price"] < 0:
        add_info["message"] = "The set price cannot be negative!"
        return http.HttpResponse(add_info)
    entry_images = dict_data['pictures']
    save_tag = transaction.savepoint()
    try:
        with transaction.atomic():
            del dict_data['pictures']
            ## add into the entry info
            entry_info = Entry.objects.create(**dict_data)
            ## add into the entry info
            for index in range(len(entry_images)):
                new_entry_image = EntryImage()
                new_entry_image.entry_id = entry_info
                new_entry_image.image_id = index + 1
                new_entry_image.image = entry_images[index]
                new_entry_image.save()
            add_info["success"] = 1
    except Exception as e:
        transaction.savepoint_rollback(save_tag)
        add_info["message"] = "Add error!"
    return http.JsonResponse(add_info)

#delete the book entry permanently
##not delete but set the seller inventory to be -1 so that it cannot be seen by any sides except managers
##avoid the problem of delete cascade
@transaction.atomic
def delete_book_entry(request):
    book_delete_permit = json.loads(request.body, strict = False)
    delete_info = {"success":0, "message":""}
    save_tag = transaction.savepoint()
    try:
        with transaction.atomic():
            entry_info = Entry.objects.get(book_delete_permit["entry_id"])
            entry_info.customer_inventory = -1
            entry_info.seller_inventory = -1
            entry_info.save()
            delete_info["success"] = 1
    except Exception as e:
        delete_info["message"] = "Delete Error!"
        transaction.savepoint_rollback(save_tag)
    return http.JsonResponse(delete_info)

#update the book information
@transaction.atomic
def update_book_entry(request):
    pass

def book_summary(request):
    #randomly show 10 books on the main page
    pass

def book_detail(request, pk):
    #show the detail information of one book
    pass

#search the book vaguely in the text
def search_book(request):
    pass






