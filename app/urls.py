from django.urls import path, re_path
from app import views

app_name='app'




urlpatterns = [
    path('', views.index, name='home'),
    path('properties', views.properties, name='properties'),   
]
