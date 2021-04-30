from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django.contrib.auth.models import User
#from .models import Profile, Ticket, Order
#from .forms import ProfileForm, UserForm, TicketForm






# ----------------------------------------------------- index -----------------

@login_required()
def index(request):

    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))
