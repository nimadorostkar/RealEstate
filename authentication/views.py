from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse, HttpResponseRedirect, request
from .forms import LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required
from blogApp.models import Post, Categories, PostComment
from app import models
from app.models import Profile
from django.contrib import messages




#------------------------------------------------------------------------------
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'اطلاعات معتبر نیست'
        else:
            msg = 'خطا در تأیید فرم'

    return render(request, "accounts/login.html", {"form": form, "msg" : msg })









#------------------------------------------------------------------------------
def register_user(request):
    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'کاربر ایجاد شد - <a href="/login">ورود</a>.'
            success = True

            #return redirect("/login/")

        else:
            msg = 'اطلاعات فرم معتبر نیست'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })













#------------------------------------------------------------------------------
@login_required(login_url='/login')
def password_change(request):
    current_user = request.user
    if request.method == 'POST':
        current_user.set_password(request.POST['new_password'])
        current_user.save()
        change_done = "رمز عبور با موفقیت تغییر یافت"
        context = {'current_user': current_user, 'change_done':change_done }
        return render(request, 'accounts/passchange.html', context)

    context = {'current_user': current_user }
    return render(request, 'accounts/passchange.html', context)










# End
