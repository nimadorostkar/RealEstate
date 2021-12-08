from django.urls import path, re_path
from crm import views
from .views import customers, products, order_requests
from django.contrib.auth.decorators import login_required



urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path('etc', views.etc, name='etc'),
    path('search',views.search,name='search'),
    # Product
    path('products', login_required(products.as_view()), name='products'),
    path('product_detail/<int:id>/',views.product_detail,name='product_detail'),
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
    path('order_invoice/<int:id>/', views.order_invoice, name='order_invoice'),
]
