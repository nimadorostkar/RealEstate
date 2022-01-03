from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from . import models
from .models import Profile, Item, Slider, ItemImage, Area, Fav, Contact
from blogApp.models import Post, Categories, PostComment
from .forms import ProfileForm, UserForm, ContactForm
from django.db.models import Count, Max, Min, Avg, Q
from itertools import chain
from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
from django.views import generic
from django.contrib.auth.forms import PasswordChangeForm





#------------------------------------------------------------------------------
def index(request):
    img = models.Slider.objects.all()
    item_img = models.ItemImage.objects.all()
    items = models.Item.objects.filter(available=True).order_by("-date")[:11]
    all_items_count = models.Item.objects.filter(available=True).count()
    all_area_count = models.Area.objects.all().count()
    areas = models.Area.objects.all()
    fav = models.Fav.objects.all()
    context = {'img':img,
    'items':items,
    'item_img':item_img,
    'areas':areas,
    'fav':fav,
    'all_items_count':all_items_count,
    'all_area_count':all_area_count}
    return render(request, 'index.html', context)




#------------------------------------------------------------------------------
def search(request):
    areas = models.Area.objects.all()
    if request.method=="POST":
        search_buy_status = request.POST['buy_status']
        search_estate_status = request.POST['estate_status']
        search_area = request.POST['area']
        #
        search_rent = request.POST['rent']
        search_rent_rage = search_rent.split(',')
        #
        search_mortgage = request.POST['mortgage']
        search_mortgage_rage = search_mortgage.split(',')
        #
        search_price = request.POST['price']
        search_price_rage = search_price.split(',')
        #
        search_area_size = request.POST['area_size']
        search_area_size_rage = search_area_size.split(',')


        if search:
            general_match = models.Item.objects.filter( Q(buy_status__icontains=search_buy_status) & Q(area__name__icontains=search_area) & Q(estate_status__icontains=search_estate_status)  )
            partial_match = models.Item.objects.filter( Q(area_size__range=(search_area_size_rage[0],search_area_size_rage[1])) )

            if search_buy_status == 'رهن و اجاره':
                price_match = models.Item.objects.filter( Q(rent__range=(search_rent_rage[0],search_rent_rage[1])) & Q(deposit__range=(search_mortgage_rage[0],search_mortgage_rage[1])) )
            elif search_buy_status == 'فروش':
                price_match = models.Item.objects.filter( Q(price__range=(search_price_rage[0],search_price_rage[1])) )
            elif search_buy_status == 'رهن کامل':
                price_match = models.Item.objects.filter( Q(deposit__range=(search_mortgage_rage[0],search_mortgage_rage[1])) )
            elif search_buy_status == 'پیش فروش':
                price_match = models.Item.objects.filter( Q(price__range=(search_price_rage[0],search_price_rage[1])) )
            else:
                price_match = models.Item.objects.filter( Q(rent__range=(search_rent_rage[0],search_rent_rage[1])) & Q(deposit__range=(search_mortgage_rage[0],search_mortgage_rage[1])) & Q(price__range=(search_price_rage[0],search_price_rage[1]))  )

            match = list(chain(general_match & partial_match & price_match ))

            if match:
                return render(request,'search.html', {'sr': match, 'areas':areas })
            else:
                messages.error(request,  '   چیزی یافت نشد ، لطفا مجددا جستجو کنید ' )
        else:
            return HttpResponseRedirect('/search')
    return render(request, 'search.html', {'areas':areas })






#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def profile(request):
    current_user = request.user
    profile = models.Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        current_user.username = request.POST['user']
        current_user.first_name = request.POST['firstname']
        current_user.last_name = request.POST['lastname']
        profile.phone = request.POST['phone']
        current_user.email = request.POST['email']
        profile.additional_information = request.POST['additional_information']
        if (request.FILES): profile.user_photo = request.FILES['photo']
        current_user.save()
        profile.save()
        return HttpResponseRedirect('/profile')

    context = {}
    return render(request, 'accounts/profile.html', context)











#------------------------------------------------------------------------------
class items(generic.ListView):
    model = Item
    template_name = 'items.html'
    context_object_name = 'items'
    queryset = Item.objects.filter(available=True)
    ordering = ['-date']
    paginate_by = 16

    def get_context_data(self, *args, **kwargs):
        areas = Area.objects.all()
        context = super(items, self).get_context_data(*args, **kwargs)
        context["areas"] = areas
        return context



def items_detail(request, id):
    Item = get_object_or_404(models.Item, id=id)
    item_img = models.ItemImage.objects.filter(item=Item)
    similar_items = models.Item.objects.filter(available=True, area=Item.area).order_by("-date")

    item_sales_expert = get_object_or_404(models.Profile, user=Item.sales_expert)

    if request.user.is_authenticated:
        item_fav = list(models.Fav.objects.filter(user=request.user).values_list('item', flat=True))
        if (Item.id in item_fav):
            if request.method=="POST":
                obj = get_object_or_404(models.Fav, item=Item.id)
                obj.delete()
                return redirect(Item.get_absolute_url())
        else:
            if request.method == 'POST':
                obj = Fav()
                obj.user = request.user
                obj.item = Item
                obj.save()
                return redirect(Item.get_absolute_url())
    else:
        item_fav=""
    context = {'Item':Item , 'item_img':item_img , 'similar_items':similar_items, 'item_fav':item_fav , 'item_sales_expert':item_sales_expert , 'domain': request.get_host() }
    return render(request, 'items_detail.html', context)









#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def favs(request):
    favs = models.Fav.objects.filter(user=request.user)
    areas = models.Area.objects.all()
    context = {'favs':favs, 'areas':areas}
    context['segment'] = 'items'
    html_template = loader.get_template( 'favs.html' )
    return HttpResponse(html_template.render(context, request))








#------------------------------------------------------------------------------
def contact(request):
    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            obj = Contact()
            obj.name = contact_form.cleaned_data['name']
            obj.phone = contact_form.cleaned_data['phone']
            obj.body = contact_form.cleaned_data['body']
            obj.save()
    else:
        contact_form = ContactForm(data=request.POST)

    context = {'contact_form':contact_form}
    context['segment'] = 'contact'
    html_template = loader.get_template( 'contact.html' )
    return HttpResponse(html_template.render(context, request))















# End
