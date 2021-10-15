from django.urls import path, re_path
from app import views

app_name='app'

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    # etc
    path('profile', views.profile, name='profile'),
    path('contact', views.contact, name='contact'),
    path('search',views.search,name='search'),
    path('favs', views.favs, name='favs'),
    # Items
    path('items', views.items, name='items'),
    path('items_detail/<int:id>/',views.items_detail,name='items_detail'),
]
