from django.conf.urls import url
from user import views_book, views_mgmt, views_order, views_user
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
    url('^order_book',views_order.order_book),
    url('^confirm_order',views_order.confirm_order_book),
    url('^order_of/(?P<pk>\d+)', views_order.order_of),
    url('^pack_book_update', views_order.pack_book_update),
    url('^confirm_receive',views_order.receive_book_confirm),
    #user
    url('^user_info', views_user.user_info),
    url('^user_order_all', views_user.user_order_all),
    url('^user_order_detail/(?P<pk>\d+)', views_user.user_order_detail),
    url('^user_order_deliver', views_user.user_order_deliver),
    url('^user_order_transport', views_user.user_order_transport),
    url('^edit_user_info', views_user.edit_user_info),
    url('^entry_comment', views_user.entry_comment),
    url('^entry_feedback', views_user.entry_feedback),
    #test
    url('^test_view_order_info',views_order.test_view_order_info)
]
