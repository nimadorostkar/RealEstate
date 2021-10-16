from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from . import models
from .models import Profile, Item, Slider, ItemImage, Area, Fav
from blogApp.models import Post, Categories, PostComment
from .forms import ProfileForm, UserForm
from django.db.models import Count, Max, Min, Avg, Q
from itertools import chain
from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from django.contrib import messages





#------------------------------------------------------------------------------
def index(request):
    img = models.Slider.objects.all()
    item_img = models.ItemImage.objects.all()
    items = models.Item.objects.all().order_by("-date")[:11]
    areas = models.Area.objects.all()
    fav = models.Fav.objects.all()
    context = {'img':img, 'items':items, 'item_img':item_img, 'areas':areas, 'fav':fav}
    context['segment'] = 'index'
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))




#------------------------------------------------------------------------------
def search(request):
    areas = models.Area.objects.all()
    if request.method=="POST":
        search_buy_status = request.POST['buy_status']
        search_text = request.POST['text']
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

        '''
        if request.POST.get('parking'):
            search_parking = True
        else:
            search_parking = False

        if request.POST.get('elevator'):
            search_elevator = True
        else:
            search_elevator = False

        if request.POST.get('storage_room'):
            search_storage_room = True
        else:
            search_storage_room = False
        '''

        if search:
            general_match = models.Item.objects.filter( Q(buy_status__icontains=search_buy_status) & Q(area__name__icontains=search_area) & Q(additional_information__icontains=search_text) )
            partial_match = models.Item.objects.filter( Q(area_size__range=(search_area_size_rage[0],search_area_size_rage[1])) )
            #checkbox_match = models.Item.objects.filter( Q(parking=search_parking) & Q(elevator=search_elevator) & Q(storage_room=search_storage_room) )
            if search_buy_status == 'اجاره':
                price_match = models.Item.objects.filter( Q(rent__range=(search_rent_rage[0],search_rent_rage[1])) & Q(deposit__range=(search_mortgage_rage[0],search_mortgage_rage[1])) )
            elif search_buy_status == 'خرید':
                price_match = models.Item.objects.filter( Q(price__range=(search_price_rage[0],search_price_rage[1])) )
            elif search_buy_status == 'رهن':
                price_match = models.Item.objects.filter( Q(deposit__range=(search_mortgage_rage[0],search_mortgage_rage[1])) )
            else:
                price_match = models.Item.objects.filter( Q(rent__range=(search_rent_rage[0],search_rent_rage[1])) & Q(deposit__range=(search_mortgage_rage[0],search_mortgage_rage[1])) & Q(price__range=(search_price_rage[0],search_price_rage[1])) )

            match = list(chain(general_match & partial_match & price_match ))

            if match:
                return render(request,'search.html', {'sr': match})
            else:
                messages.error(request,  '   چیزی یافت نشد ، لطفا مجددا جستجو کنید ' )
        else:
            return HttpResponseRedirect('/search')
    return render(request, 'search.html', {'areas':areas})




#------------------------------------------------------------------------------

@login_required(login_url="/login/")
def profile(request):
    profile = models.Profile.objects.filter(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data['username']
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            email = user_form.cleaned_data['email']
            password1 = user_form.cleaned_data['password1']
            password2 = user_form.cleaned_data['password2']
            phone = profile_form.cleaned_data['phone']
            address = profile_form.cleaned_data['address']
            user_photo = profile_form.cleaned_data['user_photo']
            user_form.save()
            profile_form.save()
            context = {'user_form':user_form, 'profile_form':profile_form }
            context['segment'] = 'profile'

            html_template = loader.get_template( 'accounts/profile.html' )
            return HttpResponse(html_template.render(context, request))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {'user_form':user_form, 'profile_form':profile_form}
    context['segment'] = 'profile'

    html_template = loader.get_template( 'accounts/profile.html' )
    return HttpResponse(html_template.render(context, request))






#------------------------------------------------------------------------------
def items(request):
    items = models.Item.objects.all().order_by("-date")
    areas = models.Area.objects.all()
    latestpost_list = Post.objects.all().order_by('-post_date')[:3]
    context = {'items':items, 'areas':areas, 'latestpost_list':latestpost_list}
    context['segment'] = 'items'
    html_template = loader.get_template( 'items.html' )
    return HttpResponse(html_template.render(context, request))



def items_detail(request, id):
    Item = get_object_or_404(models.Item, id=id)
    item_img = models.ItemImage.objects.filter(item=Item)
    similar_items = models.Item.objects.filter(area=Item.area).order_by("-date")

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
    context = {'Item':Item , 'item_img':item_img , 'similar_items':similar_items, 'item_fav':item_fav}
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
    context = {}
    context['segment'] = 'contact'
    html_template = loader.get_template( 'contact.html' )
    return HttpResponse(html_template.render(context, request))




# End
