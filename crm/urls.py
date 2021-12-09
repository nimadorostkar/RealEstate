from django.urls import path, re_path
from crm import views
from .views import customers, order_requests, crm_items
from django.contrib.auth.decorators import login_required



urlpatterns = [
    # The home page
    path('', views.index, name='crm'),
    path('etc', views.etc, name='etc'),
    path('search',views.search,name='search'),
    # Product
    path('crm_items', crm_items.as_view(), name='crm_items'),
    path('crm_items_detail/<int:id>/',views.crm_items_detail,name='crm_items_detail'),
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
]
