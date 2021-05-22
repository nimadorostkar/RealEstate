from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django.contrib.auth.models import User
from .models import Item
#from .forms import ProfileForm, UserForm, TicketForm






# ----------------------------------------------------- index -----------------
@login_required()
def index(request):
    items = models.Item.objects.all()
    context = { 'items': items }
    return render(request, 'index.html', context)




# --------------------------------------------------- properties --------------
@login_required()
def items(request):
    items = models.Item.objects.all()
    context = { 'items': items }
    return render(request, 'items.html', context)



# --------------------------------------------------- properties --------------
@login_required()
def items_detail(request, id):
    item = get_object_or_404(models.Item, id=id)
    context = { 'item': item }
    return render(request, 'items_detail.html', context)





# End
