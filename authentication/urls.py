from django.urls import path
from .views import login_view, register_user, password_change
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('password_change/', password_change, name="password_change"),
]
