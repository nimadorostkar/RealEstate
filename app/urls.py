from django.urls import path, re_path
from app import views

app_name='app'

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path('profile', views.profile, name='profile'),
    path('items', views.items, name='items'),
    path('items_detail/<int:id>/',views.items_detail,name='items_detail'),
]
