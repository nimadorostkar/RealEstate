from django.urls import path, re_path
from app import views

app_name='app'

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('profile', views.profile, name='profile'),
    re_path(r'^.*\.*', views.pages, name='pages'),

]
