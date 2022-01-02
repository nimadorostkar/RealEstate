from django.urls import path, re_path
from crm import views
from .views import customers, order_requests, crm_items, crm_blog
from django.contrib.auth.decorators import login_required



urlpatterns = [
    # The home page
    path('', views.index, name='crm'),
    path('etc', views.etc, name='etc'),
    path('search',views.search,name='search'),
    path('sales_expert_registration', views.sales_expert_registration, name='sales_expert_registration'),
    path('addarea', views.addarea, name='addarea'),
    # Items
    path('crm_items', login_required(crm_items.as_view()), name='crm_items'),
    path('crm_items_detail/<int:id>/',views.crm_items_detail,name='crm_items_detail'),
    path('crm_item_edit/<int:id>/', views.crm_item_edit, name='crm_item_edit'),
    path('rahnoejare_registration', views.rahnoejare_registration, name='rahnoejare_registration'),
    path('rahn_registration', views.rahn_registration, name='rahn_registration'),
    path('froosh_registration', views.froosh_registration, name='froosh_registration'),
    path('pishfroosh_registration', views.pishfroosh_registration, name='pishfroosh_registration'),
    path('addFileImg', views.addFileImg, name='addFileImg'),
    path('deleteImg/<int:id>/',views.deleteImg,name='deleteImg'),
    # Customer
    path('customers', login_required(customers.as_view()), name='customers'),
    path('customer_detail/<int:id>/',views.customer_detail,name='customer_detail'),
    path('customer_registration', views.customer_registration, name='customer_registration'),
    path('customer_edit/<int:id>/', views.customer_edit, name='customer_edit'),
    # Order
    path('order_requests', login_required(order_requests.as_view()), name='order_requests'),
    path('order_req_detail/<int:id>/',views.order_req_detail,name='order_req_detail'),
    path('order_registration', views.order_registration, name='order_registration'),
    path('order_edit/<int:id>/', views.order_edit, name='order_edit'),
    path('incoming_remove', views.incoming_remove, name='incoming_remove'),
    # Settings
    path('settings_edit', views.settings_edit, name='settings_edit'),
    path('logoupload', views.logoupload, name='logoupload'),
    path('headerupload', views.headerupload, name='headerupload'),
    # Blog
    path('crm_blog', crm_blog.as_view(), name='crm_blog'),
    path('post_registration', views.post_registration, name='post_registration'),
    path('crm_post_edit',views.crm_post_edit,name='crm_post_edit'),
    path('crm_post_edit_done',views.crm_post_edit_done,name='crm_post_edit_done'),
    path('post_cat',views.post_cat,name='post_cat'),
    # Contact
    path('contacts', views.contacts, name='contacts'),
    path('contact_detail/<int:id>/', views.contact_detail, name='contact_detail'),
]
