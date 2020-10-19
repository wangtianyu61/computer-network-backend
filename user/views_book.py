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
import random

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
    return http.JsonResponse({"book_info":all_entry_info})

# add the book entry for the seller
@transaction.atomic
def add_book_entry(request):
    book_info = json.loads(request.body, strict = False)
    add_info = {"success":0, "message":""} 
    ## check the logic
    if "original_price" in book_info.keys() and book_info["original_price"] < 0:
        add_info["message"] = "The original price cannot be negative!"
        return http.JsonResponse(add_info)
    if book_info["price"] < 0:
        add_info["message"] = "The set price cannot be negative!"
        return http.JsonResponse(add_info)
    if book_info["inventory"] < 0:
        add_info["message"] = "The inventory cannot be negative!"
        return http.JsonResponse(add_info)
    entry_images = book_info['pictures']
    save_tag = transaction.savepoint()
    try:
        with transaction.atomic():
            del book_info['pictures']
            ## add into the entry info
            entry_info = Entry()
            entry_info.seller_id = book_info['seller_id']
            entry_info.name = book_info['name']
            entry_info.author = book_info['author']
            entry_info.category = book_info['category']
            entry_info.original_price = book_info['original_price']
            entry_info.price = book_info['price']
            entry_info.description = book_info['description']
            entry_info.customer_inventory = book_info['inventory']
            entry_info.seller_inventory = book_info['inventory']
            #check for the manager
            entry_info.status = 1
            entry_info.save()
            #entry_info = Entry.objects.create(**dict_data)
            ## add into the entry info
            for index in range(len(entry_images)):
                new_entry_image = EntryImage()
                new_entry_image.entry_id = entry_info
                new_entry_image.image_id = index + 1
                new_entry_image.image = entry_images[index]
                new_entry_image.save()
            add_info["success"] = 1
    except Exception as e:
        print(e)
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
    book_update_permit = json.loads(request.body, strict = False)
    update_info ={"success":0, "message":""}
    if book_update_permit["price"] < 0:
        update_info["message"] = "The set price cannot be negative!"
        return http.JsonResponse(update_info)
    if book_update_permit["update_number"] < 0:
        update_info["message"] = "The inventory cannot be negative!"
        return http.JsonResponse(update_info)
    save_tag = transaction.savepoint()
    #change the inventory
    try:
        with transaction.atomic():
            update_entry = Entry.objects.get(entry_id = book_update_permit["entry_id"])
            change_num = book_update_permit["update_number"] - update_entry.customer_inventory
            if change_num + update_entry.seller_inventory < 0:
                update_info["message"] = "The inventory cannot be negative!"
                return http.JsonResponse(update_info)
            update_entry.customer_inventory = book_update_permit["update_number"]
            update_entry.seller_inventory = change_num + update_entry.seller_inventory
            update_entry.price = book_update_permit["price"]
            update_entry.description = book_update_permit["description"]
            update_entry.save()
            update_info["success"] = 1
    except Exception as e:
        update_info["message"] = "Update Error!"
        transaction.savepoint_rollback(update_info)
    return http.JsonResponse(update_info)

def book_summary(request):
    #randomly show 10 books on the main page
    available_book = Entry.objects.filter(customer_inventory__gte = 0)
    #too few books
    if len(available_book) < show_number:
        random_entries = available_book
    else:
        available_entry_id = [entry.entry_id for entry in available_book]
        random_entries_id = random.sample(available_entry_id, show_number)
        random_entries = [Entry.objects.get(entry_id = random_entry_id) for random_entry_id in random_entries_id]

    book_info = []
    for select_entry in random_entries:
        entry_info = {"entry_id":select_entry.entry_id,
                        "name":select_entry.name,
                        "author":select_entry.author,
                        "category":select_entry.category,
                        "price":select_entry.price,
                        "original_price":select_entry.original_price,
                        "inventory":select_entry.customer_inventory}
        book_info.append(entry_info)
    return http.JsonResponse({"book_info":book_info})

def book_detail(request, pk):
    #show the detail information of one book
    entry_info = Entry.objects.get(entry_id = pk)
    entry_detail = {"entry_id":entry_info.entry_id, "name":entry_info.name, "author":entry_info.author,
                    "price":entry_info.price, "original_price":entry_info.original_price,"category":entry_info.category,
                    "description":entry_info.description, "inventory":entry_info.customer_inventory}
    entry_images = EntryImage.objects.filter(entry_id = pk)
    entry_detail["image"] = [entry_image.image for entry_image in entry_images]
    entry_detail["entry_comment"] = []
    entry_comments = EntryComment.objects.filter(entry_id = pk)
    for comment_item in entry_comments:
        comment_detail = {"comment_time":comment_item.comment_time, "entry_comment":comment_item.entry_comment,
                            "entry_feedback":comment_item.entry_feedback}
        entry_detail["entry_comment"].append(comment_detail)
    return http.JsonResponse(entry_detail)


#search the book vaguely in the text
def search_book(request):
    #add into one type
    pass

#search the book by type:
def search_book_type(request):
    pass






