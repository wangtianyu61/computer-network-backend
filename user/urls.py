from django.conf.urls import url
from user import views_book, views_mgmt
urlpatterns = [
    #management
    url('^register', views_mgmt.user_register),
    url('^login', views_mgmt.user_login),
    #book
    url('^book_of/(?P<pk>\d+)', views_book.book_of),
    url('^add_book_entry', views_book.add_book_entry),
    url('^delete_book_entry', views_book.delete_book_entry),
    url('^update_book_entry', views_book.update_book_entry),
    url('^book$', views_book.book_summary),
    url('^book/(?P<pk>\d+)', views_book.book_detail),
    url('^search_book',views_book.search_book),
    #order
    url('^order_book',views_order.order_book)
]