from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from django.contrib.auth.models import User
from .models import Settings
from blogApp.models import Post, Categories, PostComment





def settings(request):
    return {
    'settings': models.Settings.objects.all().last() ,
    'latestpost_list' : Post.objects.all().order_by('-post_date')[:3] ,
    'footer_latestpost_list' : Post.objects.all().order_by('-post_date')[:2]
    }
