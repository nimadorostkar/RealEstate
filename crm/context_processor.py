from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from django.contrib.auth.models import User
from .models import Order_request






def notification(request):
    return {
       'new_reqs': models.Order_request.objects.filter(status='جدید').order_by('-date_created') ,
       'new_req_counts': models.Order_request.objects.filter(status='جدید').count()
    }
