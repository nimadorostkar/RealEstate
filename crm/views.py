from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from django.contrib.auth.models import User
from .models import Order_request, Order_incomings
from .forms import TimeForm
from itertools import chain
from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from django.db.models import Q
import datetime
import jdatetime
from django.contrib import messages
from django.views import generic
from django.utils.decorators import method_decorator
from allauth.utils import generate_unique_username
from app.models import Item, Profile, Area, ItemImage, Ownership
from django.contrib.auth.decorators import user_passes_test




#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def index(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :

        now = jdatetime.datetime.now()

        if request.user.is_superuser:
            open_reqs_count = models.Order_request.objects.all().exclude(status='تکمیل شده').count()
            customers_count = models.Profile.objects.filter( Q(user_type='کاربر') | Q(user_type='کاربر ویژه') ).count()
            items_count = models.Item.objects.all().count()
            new_order_count = models.Order_request.objects.filter(status='جدید').count()

            incomings = models.Order_incomings.objects.all()
            chart = []
            for Incoming in incomings:
                if Incoming.date_created.year == now.year and Incoming.date_created.month == now.month and Incoming.date_created.day == now.day:
                    chart.append(Incoming)
        else:
            open_reqs_count = models.Order_request.objects.filter(user=uProfile).exclude(status='تکمیل شده').count()
            customers_count = models.Profile.objects.filter( Q(user_type='کاربر') | Q(user_type='کاربر ویژه') and Q(sales_expert=uProfile ) ).count()
            items_count = models.Item.objects.filter(sales_expert=request.user).count()
            new_order_count = models.Order_request.objects.filter( status='جدید' , user=uProfile ).count()

            incomings = models.Order_incomings.objects.filter(user=uProfile)
            chart = []
            for Incoming in incomings:
                if Incoming.date_created.year == now.year and Incoming.date_created.month == now.month and Incoming.date_created.day == now.day:
                    chart.append(Incoming)



        context = {'open_reqs_count': open_reqs_count, 'customers_count':customers_count , 'items_count':items_count, 'new_order_count':new_order_count, 'chart':chart, 'now':now }

        html_template = loader.get_template('crm/home/index.html')
        return HttpResponse(html_template.render(context, request))

    else:
        return redirect("/")









#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def etc(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :

        context = {'segment': 'etc'}

        html_template = loader.get_template('crm/home/etc.html')
        return HttpResponse(html_template.render(context, request))

    else:
        return redirect("/")










#------------------------------------------------------------------------------
@login_required
def search(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :

        reqs = Order_request.objects.all()

        if request.method=="POST":
            search = request.POST['q']
            if search:
                customer = models.Profile.objects.filter( Q(user__username__icontains=search) | Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) | Q(additional_information__icontains=search) | Q(phone__icontains=search) | Q(user__email__icontains=search) )
                item = models.Item.objects.filter( Q(ownership__name__icontains=search) | Q(area__name__icontains=search) | Q(buy_status__icontains=search) | Q(estate_status__icontains=search) | Q(code__icontains=search)  | Q(additional_information__icontains=search) )
                return render(request,'crm/home/search.html', {'customer':customer, 'item':item, 'reqs':reqs})
            else:
                return HttpResponseRedirect('/search')
        return render(request, 'crm/home/search.html', {})

    else:
        return redirect("/")








#------------------------------------------------------------------------------
class crm_items(generic.ListView):
    model = Item
    template_name = 'crm/home/items.html'
    context_object_name = 'items'
    queryset = Item.objects.all()
    ordering = ['-date']
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        uProfile = get_object_or_404(models.Profile, user=self.request.user)
        if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :
            context = super(crm_items, self).get_context_data(*args, **kwargs)
            context["uProfile"] = uProfile
            return context
        else:
            return redirect('crm')






@login_required()
def crm_items_detail(request, id):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :
        item = get_object_or_404(models.Item, id=id)
        if item.sales_expert == request.user or uProfile.user_type=="مدیر" :
            images = ItemImage.objects.filter(item=item)
            reqs = models.Order_request.objects.filter(item=item).order_by('-date_created')
            context = {'item':item, 'images':images, 'reqs':reqs}
            return render(request, 'crm/home/items_detail.html', context)
        else:
            return redirect("crm_items")
    else:
        return redirect("/")








@login_required()
def addFileImg(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :
        item = get_object_or_404(models.Item, id=request.POST['item'])

        newImg=ItemImage()
        newImg.item = item
        newImg.Image = request.FILES['img']
        newImg.save()

        images = ItemImage.objects.filter(item=item)
        reqs = models.Order_request.objects.filter(item=item).order_by('-date_created')

        context = {'item':item, 'images':images, 'reqs':reqs}
        return render(request, 'crm/home/items_detail.html', context)

    else:
        return redirect("/")







@login_required()
def deleteImg(request, id):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :
        img = get_object_or_404(ItemImage, id=id)
        img.delete()
        #return HttpResponseRedirect('crm/crm_items_detail/{}/'.format(img.item.id))
        return redirect('crm_items_detail', id=img.item.id)
    else:
        return redirect("/")







#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def crm_item_edit(request, id):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :
        item = get_object_or_404(models.Item, id=id)
        area = Area.objects.all()

        if request.method=="POST":
            if request.POST.get('remove'):
                item.delete()
                return redirect('crm_items')
            else:
                if request.POST.get('available'):
                    available = True
                else:
                    available = False

                if request.POST.get('parking'):
                    parking = True
                else:
                    parking = False

                if request.POST.get('storage_room'):
                    storage_room = True
                else:
                    storage_room = False

                if request.POST.get('elevator'):
                    elevator = True
                else:
                    elevator = False

                if request.POST.get('balcony'):
                    balcony = True
                else:
                    balcony = False

                owner = item.ownership
                owner.name = request.POST['owner_name']
                owner.phone = request.POST['owner_phone']
                owner.save()

                item.available = available
                item.code = request.POST['code']
                item.estate_status = request.POST['estate_status']
                item.area_size = request.POST['area_size']
                item.room_qty = request.POST['room_qty']
                item.building_age = request.POST['building_age']
                item.parking = parking
                item.storage_room = storage_room
                item.elevator = elevator
                item.balcony = balcony

                if item.buy_status == 'فروش':
                    item.price = request.POST['price']
                elif item.buy_status == 'پیش فروش':
                    item.price = request.POST['price']
                elif item.buy_status == 'رهن و اجاره':
                    item.deposit = request.POST['deposit']
                    item.rent = request.POST['rent']
                elif item.buy_status == 'رهن کامل':
                    item.deposit = request.POST['deposit']

                item.area = get_object_or_404(Area, id=request.POST['area'])
                item.additional_information = request.POST['additional_information']
                if (request.FILES): item.image = request.FILES['img']
                item.video_link = request.POST['video']
                item.sales_expert = request.user
                item.ownership = owner
                item.save()

                success = 'ویرایش فایل انجام شد ، مشاهده صفحه فایل'

                context = {'area':area, 'success':success, 'link':item}
                return render(request, 'crm/home/crm_item_edit.html', context)



        context = {'item':item, 'area':area}
        html_template = loader.get_template('crm/home/crm_item_edit.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect("/")












#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def rahnoejare_registration(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :

        area = Area.objects.all()
        defaultcode = (Item.objects.all().last().id)+1
        if request.method=="POST":

            if request.POST.get('available'):
                available = True
            else:
                available = False

            if request.POST.get('parking'):
                parking = True
            else:
                parking = False

            if request.POST.get('storage_room'):
                storage_room = True
            else:
                storage_room = False

            if request.POST.get('elevator'):
                elevator = True
            else:
                elevator = False

            if request.POST.get('balcony'):
                balcony = True
            else:
                balcony = False

            owner = Ownership()
            owner.name = request.POST['owner_name']
            owner.phone = request.POST['owner_phone']
            owner.save()

            item = Item()
            item.available = available
            item.code = request.POST['code']
            item.buy_status = 'رهن و اجاره'
            item.estate_status = request.POST['estate_status']
            item.area_size = request.POST['area_size']
            item.room_qty = request.POST['room_qty']
            item.building_age = request.POST['building_age']
            item.parking = parking
            item.storage_room = storage_room
            item.elevator = elevator
            item.balcony = balcony
            item.deposit = request.POST['deposit']
            item.rent = request.POST['rent']
            item.area = get_object_or_404(Area, id=request.POST['area'])
            item.additional_information = request.POST['additional_information']
            if (request.FILES): item.image = request.FILES['img']
            item.video_link = request.POST['video']
            item.sales_expert = request.user
            item.ownership = owner
            item.save()

            success = 'فایل جدید ایجاد شد ، مشاهده صفحه فایل'
            link = get_object_or_404(models.Item, id=item.id)

            context = {'area':area, 'success':success, 'link':link}
            return render(request, 'crm/home/rahnoejare_registration.html', context)

        context = {'area':area, 'defaultcode':defaultcode}
        html_template = loader.get_template('crm/home/rahnoejare_registration.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect("/")





#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def rahn_registration(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :
        area = Area.objects.all()
        defaultcode = (Item.objects.all().last().id)+1
        if request.method=="POST":

            if request.POST.get('available'):
                available = True
            else:
                available = False

            if request.POST.get('parking'):
                parking = True
            else:
                parking = False

            if request.POST.get('storage_room'):
                storage_room = True
            else:
                storage_room = False

            if request.POST.get('elevator'):
                elevator = True
            else:
                elevator = False

            if request.POST.get('balcony'):
                balcony = True
            else:
                balcony = False

            owner = Ownership()
            owner.name = request.POST['owner_name']
            owner.phone = request.POST['owner_phone']
            owner.save()

            item = Item()
            item.available = available
            item.code = request.POST['code']
            item.buy_status = 'رهن کامل'
            item.estate_status = request.POST['estate_status']
            item.area_size = request.POST['area_size']
            item.room_qty = request.POST['room_qty']
            item.building_age = request.POST['building_age']
            item.parking = parking
            item.storage_room = storage_room
            item.elevator = elevator
            item.balcony = balcony
            item.deposit = request.POST['deposit']
            item.area = get_object_or_404(Area, id=request.POST['area'])
            item.additional_information = request.POST['additional_information']
            if (request.FILES): item.image = request.FILES['img']
            item.video_link = request.POST['video']
            item.sales_expert = request.user
            item.ownership = owner
            item.save()

            success = 'فایل جدید ایجاد شد ، مشاهده صفحه فایل'
            link = get_object_or_404(models.Item, id=item.id)

            context = {'area':area, 'success':success, 'link':link}
            return render(request, 'crm/home/rahnoejare_registration.html', context)

        context = {'area':area, 'defaultcode':defaultcode}
        html_template = loader.get_template('crm/home/rahn_registration.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect("/")







#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def froosh_registration(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :
        area = Area.objects.all()
        defaultcode = (Item.objects.all().last().id)+1
        if request.method=="POST":

            if request.POST.get('available'):
                available = True
            else:
                available = False

            if request.POST.get('parking'):
                parking = True
            else:
                parking = False

            if request.POST.get('storage_room'):
                storage_room = True
            else:
                storage_room = False

            if request.POST.get('elevator'):
                elevator = True
            else:
                elevator = False

            if request.POST.get('balcony'):
                balcony = True
            else:
                balcony = False

            owner = Ownership()
            owner.name = request.POST['owner_name']
            owner.phone = request.POST['owner_phone']
            owner.save()

            item = Item()
            item.available = available
            item.code = request.POST['code']
            item.buy_status = 'فروش'
            item.estate_status = request.POST['estate_status']
            item.area_size = request.POST['area_size']
            item.room_qty = request.POST['room_qty']
            item.building_age = request.POST['building_age']
            item.parking = parking
            item.storage_room = storage_room
            item.elevator = elevator
            item.balcony = balcony
            item.price = request.POST['price']
            item.area = get_object_or_404(Area, id=request.POST['area'])
            item.additional_information = request.POST['additional_information']
            if (request.FILES): item.image = request.FILES['img']
            item.video_link = request.POST['video']
            item.sales_expert = request.user
            item.ownership = owner
            item.save()

            success = 'فایل جدید ایجاد شد ، مشاهده صفحه فایل'
            link = get_object_or_404(models.Item, id=item.id)

            context = {'area':area, 'success':success, 'link':link}
            return render(request, 'crm/home/rahnoejare_registration.html', context)

        context = {'area':area, 'defaultcode':defaultcode}
        html_template = loader.get_template('crm/home/froosh_registration.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect("/")






#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def pishfroosh_registration(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :
        area = Area.objects.all()
        defaultcode = (Item.objects.all().last().id)+1
        if request.method=="POST":

            if request.POST.get('available'):
                available = True
            else:
                available = False

            if request.POST.get('parking'):
                parking = True
            else:
                parking = False

            if request.POST.get('storage_room'):
                storage_room = True
            else:
                storage_room = False

            if request.POST.get('elevator'):
                elevator = True
            else:
                elevator = False

            if request.POST.get('balcony'):
                balcony = True
            else:
                balcony = False

            owner = Ownership()
            owner.name = request.POST['owner_name']
            owner.phone = request.POST['owner_phone']
            owner.save()

            item = Item()
            item.available = available
            item.code = request.POST['code']
            item.buy_status = 'پیش فروش'
            item.estate_status = request.POST['estate_status']
            item.area_size = request.POST['area_size']
            item.room_qty = request.POST['room_qty']
            item.building_age = request.POST['building_age']
            item.parking = parking
            item.storage_room = storage_room
            item.elevator = elevator
            item.balcony = balcony
            item.price = request.POST['price']
            item.area = get_object_or_404(Area, id=request.POST['area'])
            item.additional_information = request.POST['additional_information']
            if (request.FILES): item.image = request.FILES['img']
            item.video_link = request.POST['video']
            item.sales_expert = request.user
            item.ownership = owner
            item.save()

            success = 'فایل جدید ایجاد شد ، مشاهده صفحه فایل'
            link = get_object_or_404(models.Item, id=item.id)

            context = {'area':area, 'success':success, 'link':link}
            return render(request, 'crm/home/rahnoejare_registration.html', context)

        context = {'area':area, 'defaultcode':defaultcode}
        html_template = loader.get_template('crm/home/pishfroosh_registration.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect("/")







#------------------------------------------------------------------------------
class customers(generic.ListView):
    model = Profile
    template_name = 'crm/home/customers.html'
    context_object_name = 'customers'
    queryset = Profile.objects.filter( Q(user_type='کاربر') | Q(user_type='کاربر ویژه') )
    ordering = ['-date_created']
    paginate_by = 30

    def get_context_data(self, *args, **kwargs):
        uProfile = get_object_or_404(models.Profile, user=self.request.user)
        if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :
            context = super(customers, self).get_context_data(*args, **kwargs)
            context["reqs"] = Order_request.objects.all()
            context["uProfile"] = uProfile
            return context
        else:
            return redirect('crm')











#------------------------------------------------------------------------------
@login_required()
def customer_detail(request, id):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :

        customer = get_object_or_404(models.Profile, id=id)
        if customer.sales_expert == uProfile or uProfile.user_type=="مدیر" :
            reqs = models.Order_request.objects.filter(customer=customer).order_by('-date_created')
            context = {'customer':customer, 'reqs':reqs}
            return render(request, 'crm/home/customer_detail.html', context)
        else:
            return redirect("customers")

    else:
        return redirect("/")





#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def customer_registration(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :
        if request.method=="POST":

            if request.POST.get('substantial'):
                substantial = 'کاربر ویژه'
            else:
                substantial = 'کاربر'

            first_name = request.POST['fname']
            last_name = request.POST['lname']
            email = request.POST['email']

            new_user = User()
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.email = email
            new_user.username = generate_unique_username([f'{first_name} {last_name}', email, 'new_user'])
            new_user.save()

            new_profile = get_object_or_404(models.Profile, user=new_user)
            new_profile.phone = request.POST['phone']
            new_profile.additional_information = request.POST['additional_information']
            new_profile.user_type = substantial
            new_profile.sales_expert = get_object_or_404(models.Profile, user=request.user)
            new_profile.save()

            success = 'مشتری جدید ایجاد شد ، مشاهده پروفایل'
            link = get_object_or_404(models.Profile, id=new_profile.id)

            context = {'success':success, 'link':link}
            return render(request, 'crm/home/customer_registration.html', context)

        context = {}
        html_template = loader.get_template('crm/home/customer_registration.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect("/")









#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def customer_edit(request, id):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :

        customer = get_object_or_404(models.Profile, id=id)

        if request.method=="POST":

            if request.POST.get('remove'):
                customer.delete()
                return redirect('customers')
            else:
                if request.POST.get('substantial'):
                    substantial = 'کاربر ویژه'
                else:
                    substantial = 'کاربر'

                customer.user.first_name = request.POST['fname']
                customer.user.last_name = request.POST['lname']
                customer.user.email = request.POST['email']
                customer.phone = request.POST['phone']
                customer.additional_information = request.POST['additional_information']
                customer.user_type = substantial
                customer.save()

                success = 'ویرایش اطلاعات مشتری انجام شد ، مشاهده پروفایل'
                link = get_object_or_404(models.Profile, id=customer.id)

                context = {'customer':customer, 'success':success, 'link':link}
                return render(request, 'crm/home/customer_edit.html', context)



        context = {'customer':customer}
        html_template = loader.get_template('crm/home/customer_edit.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect("/")











#------------------------------------------------------------------------------
class order_requests(generic.ListView):
    model = Order_request
    template_name = 'crm/home/order_requests.html'
    context_object_name = 'reqs'
    queryset = Order_request.objects.all()
    ordering = ['-date_created']
    paginate_by = 30

    def get_context_data(self, *args, **kwargs):
        uProfile = get_object_or_404(models.Profile, user=self.request.user)
        if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :
            context = super(order_requests, self).get_context_data(*args, **kwargs)
            context["uProfile"] = uProfile
            return context
        else:
            return redirect('crm')








@login_required()
def order_req_detail(request, id):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :

        req = get_object_or_404(models.Order_request, id=id)
        if req.user == uProfile or uProfile.user_type=="مدیر" :
            incomings = models.Order_incomings.objects.filter(request=req)
            timeform = TimeForm(request.POST)
            if request.method=="POST":
                if timeform.is_valid():
                    incoming = Order_incomings()
                    incoming.request = req
                    incoming.user = get_object_or_404(models.Profile, user=request.user)
                    incoming.date_created = timeform.cleaned_data['date_created']
                    incoming.description = request.POST['description']
                    incoming.save()
                    return redirect(req.get_absolute_url())
            context = {
            'req':req, 'incomings':incomings, 'timeform':timeform, #'total_price':total_price, 'total_incoming':total_incoming, 'remained':remained
            }
            return render(request, 'crm/home/order_req_detail.html', context)

        else:
            return redirect("order_requests")

    else:
        return redirect("/")







#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def order_registration(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :

        customers = models.Profile.objects.filter( Q(user_type='کاربر') | Q(user_type='کاربر ویژه') ).order_by('-date_created')
        items = models.Item.objects.all().order_by('-date')
        if request.method=="POST":
            req = Order_request()
            req.user = get_object_or_404(models.Profile, id=request.user.id)
            req.customer = get_object_or_404(models.Profile, id=request.POST.get('customer'))
            req.item = get_object_or_404(models.Item, id=request.POST.get('item'))
            req.description = request.POST['description']
            req.save()
            success = 'درخواست جدید ثبت شد ، مشاهده صفحه درخواست'
            context = {'customers': customers , 'items':items, 'success':success, 'link':req , 'uProfile':uProfile}
            return render(request, 'crm/home/order_registration.html', context)

        context = {'customers': customers , 'items':items , 'uProfile':uProfile}
        html_template = loader.get_template('crm/home/order_registration.html')
        return HttpResponse(html_template.render(context, request))

    else:
        return redirect("/")








#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def order_edit(request, id):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :

        req = get_object_or_404(models.Order_request, id=id)
        customers = models.Profile.objects.filter( Q(user_type='کاربر') | Q(user_type='کاربر ویژه') ).order_by('-date_created')
        items = models.Item.objects.all().order_by('-date')
        if request.method=="POST":

            if request.POST.get('remove'):
                req.delete()
                return redirect('order_requests')

            else:
                req.user = get_object_or_404(models.Profile, id=request.user.id)
                req.customer = get_object_or_404(models.Profile, id=request.POST.get('customer'))
                req.item = get_object_or_404(models.Item, id=request.POST.get('item'))
                req.description = request.POST['description']
                req.final_price = request.POST['final_price']
                req.prepayment = request.POST['prepayment']
                req.status = request.POST['status']
                req.save()

                success = 'ویرایش درخواست ثبت شد ، مشاهده درخواست'
                context = {'req':req, 'customers': customers , 'items':items, 'success':success, 'link':req , 'uProfile':uProfile}
                return render(request, 'crm/home/order_edit.html', context)

        context = {'req':req, 'customers': customers , 'items':items , 'uProfile':uProfile}
        html_template = loader.get_template('crm/home/order_edit.html')
        return HttpResponse(html_template.render(context, request))

    else:
        return redirect("/")









#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def incoming_remove(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :

        req = get_object_or_404(models.Order_request, id=request.POST['reqId'])
        incoming = get_object_or_404(models.Order_incomings, id=request.POST['incomId'])
        incoming.delete()
        return redirect(req.get_absolute_url())

    else:
        return redirect("/")








#------------------------------------------------------------------------------
@user_passes_test(lambda u: u.is_superuser)
def sales_expert_registration(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :

        if request.method=="POST":

            new_user = User()
            new_user.first_name = request.POST['fname']
            new_user.last_name = request.POST['lname']
            new_user.email = request.POST['email']
            new_user.username = request.POST['username']
            new_user.set_password(request.POST['password'])
            new_user.save()

            new_profile = get_object_or_404(models.Profile, user=new_user)
            new_profile.phone = request.POST['phone']
            new_profile.additional_information = request.POST['additional_information']
            new_profile.user_type = 'کارشناس'
            new_profile.save()

            success = 'کارشناس جدید با نام کاربری: '+ request.POST['username'] +' و رمزعبور: '+ request.POST['password'] +' ایجاد شد'
            context = {'success':success}
            return render(request, 'crm/home/sales_expert_registration.html', context)

        context = {}
        html_template = loader.get_template('crm/home/sales_expert_registration.html')
        return HttpResponse(html_template.render(context, request))

    else:
        return redirect("/")








#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def addarea(request):
    uProfile = get_object_or_404(models.Profile, user=request.user)
    if uProfile.user_type == 'کارشناس' or uProfile.user_type == 'مدیر' :

        context = {}
        if request.method=="POST":
            area = Area()
            area.name = request.POST['name']
            area.save()
            context = {'success':'منطقه جدید ایجاد شد'}

        return render(request, 'crm/home/addarea.html', context)

    else:
        return redirect("/")





















# End
