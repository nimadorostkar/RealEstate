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
from app.models import Item, Profile





#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def index(request):
    open_reqs_count = models.Order_request.objects.all().exclude(status='تکمیل شده').count()
    customers_count = models.Profile.objects.filter( Q(user_type='کاربر') | Q(user_type='کاربر ویژه') ).count()
    items_count = models.Item.objects.all().count()
    new_order_count = models.Order_request.objects.filter(status='جدید').count()

    chartList = list(models.Order_request.objects.filter(status='تکمیل شده').values_list('item_id', flat=True).distinct())
    now = jdatetime.datetime.now()
    chart = []

    for Order in chartList:
        products = models.Order_request.objects.filter(status='تکمیل شده' , product__id=Order)
        qty_sum=[0,0,0,0,0,0,0,0,0]
        for Product in products:
            if Product.date_created.year == now.year:
                if (now.month - Product.date_created.month)==0:
                    qty_sum[8] += Product.qty
                elif (now.month - Product.date_created.month)==1:
                    qty_sum[7] += Product.qty
                elif (now.month - Product.date_created.month)==2:
                    qty_sum[6] += Product.qty
                elif (now.month - Product.date_created.month)==3:
                    qty_sum[5] += Product.qty
                elif (now.month - Product.date_created.month)==4:
                    qty_sum[4] += Product.qty
                elif (now.month - Product.date_created.month)==5:
                    qty_sum[3] += Product.qty
                elif (now.month - Product.date_created.month)==6:
                    qty_sum[2] += Product.qty
                elif (now.month - Product.date_created.month)==7:
                    qty_sum[1] += Product.qty
                elif (now.month - Product.date_created.month)==8:
                    qty_sum[0] += Product.qty
        chart_product = { 'product':Product.product.name, 'qty':qty_sum}
        chart.append(chart_product)

    context = {'open_reqs_count': open_reqs_count, 'customers_count':customers_count , 'items_count':items_count, 'new_order_count':new_order_count, 'chart':chart }

    html_template = loader.get_template('crm/home/index.html')
    return HttpResponse(html_template.render(context, request))








#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def etc(request):
    context = {'segment': 'etc'}

    html_template = loader.get_template('crm/home/etc.html')
    return HttpResponse(html_template.render(context, request))








#------------------------------------------------------------------------------
@login_required
def search(request):
    if request.method=="POST":
        search = request.POST['q']
        if search:
            customer = models.Customer.objects.filter(Q(name__icontains=search) | Q(additional_information__icontains=search) | Q(phone__icontains=search) | Q(company__icontains=search) )
            product = models.Product.objects.filter(Q(name__icontains=search)  | Q(description__icontains=search) )
            order_req = models.Order_request.objects.filter(Q(customer__name__icontains=search) | Q(product__name__icontains=search) | Q(description__icontains=search))
            return render(request,'crm/home/search.html', {'customer':customer, 'product':product, 'order_req':order_req})
        else:
            return HttpResponseRedirect('/search')
    return render(request, 'crm/home/search.html', {})






#------------------------------------------------------------------------------
class crm_items(generic.ListView):
    model = Item
    template_name = 'crm/home/items.html'
    context_object_name = 'items'
    queryset = Item.objects.all()
    ordering = ['-date']
    paginate_by = 20






@login_required()
def crm_items_detail(request, id):
    item = get_object_or_404(models.Item, id=id)
    reqs = models.Order_request.objects.filter(item=item).order_by('-date_created')
    context = {'item':item, 'reqs':reqs}
    return render(request, 'crm/home/items_detail.html', context)






#------------------------------------------------------------------------------
class customers(generic.ListView):
    model = Profile
    template_name = 'crm/home/customers.html'
    context_object_name = 'customers'
    queryset = Profile.objects.all()
    ordering = ['-date_created']
    paginate_by = 30

    def get_context_data(self, *args, **kwargs):
        reqs = Order_request.objects.all()
        context = super(customers, self).get_context_data(*args, **kwargs)
        context["reqs"] = reqs
        return context







#------------------------------------------------------------------------------
@login_required()
def customer_detail(request, id):
    customer = get_object_or_404(models.Customer, id=id)
    reqs = models.Order_request.objects.filter(customer=customer).order_by('-date_created')
    context = {'customer':customer, 'reqs':reqs}
    return render(request, 'crm/home/customer_detail.html', context)





#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def customer_registration(request):
    products = models.Product.objects.all().order_by('-date_created')
    if request.method=="POST":

        if request.POST.get('substantial'):
            substantial = True
        else:
            substantial = False

        new = Customer()
        new.name = request.POST['name']
        new.phone = request.POST['phone']
        new.company = request.POST['company']
        new.address = request.POST['address']
        new.additional_information = request.POST['additional_information']
        new.substantial = substantial
        new.save()
        get_products = request.POST.getlist('products')
        for product in get_products:
           if Product.objects.all().exists():
              product = Product.objects.get(id=product)
              new.product_tag.add(product)

        success = 'مشتری جدید ایجاد شد ، مشاهده پروفایل'
        link = get_object_or_404(models.Customer, id=new.id)

        context = {'products':products, 'success':success, 'link':link}
        return render(request, 'crm/home/customer_registration.html', context)

    context = {'products':products}
    html_template = loader.get_template('crm/home/customer_registration.html')
    return HttpResponse(html_template.render(context, request))









#------------------------------------------------------------------------------
class order_requests(generic.ListView):
    model = Order_request
    template_name = 'crm/home/order_requests.html'
    context_object_name = 'reqs'
    queryset = Order_request.objects.all()
    ordering = ['-date_created']
    paginate_by = 30




@login_required()
def order_req_detail(request, id):
    req = get_object_or_404(models.Order_request, id=id)
    incomings = models.Order_incomings.objects.filter(request=req)
    #total_price = (req.product.price * req.qty) - ((req.product.price * req.qty)*(req.discount/100))
    #total_incoming = sum(incomings.values_list('amount', flat=True))
    #remained = total_price - total_incoming

    timeform = TimeForm(request.POST)
    if request.method=="POST":
        if timeform.is_valid():
            incoming = Order_incomings()
            incoming.request = req
            incoming.amount = request.POST['amount']
            incoming.date_created = timeform.cleaned_data['date_created']
            incoming.save()
            return redirect(req.get_absolute_url())


    context = {
    'req':req, 'incomings':incomings, 'timeform':timeform, #'total_price':total_price, 'total_incoming':total_incoming, 'remained':remained
    }
    return render(request, 'crm/home/order_req_detail.html', context)







#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def order_registration(request):
    customers = models.Customer.objects.all().order_by('-date_created')
    products = models.Product.objects.filter(available=True).order_by('-date_created')
    if request.method=="POST":
        req = Order_request()
        req.user = request.user
        req.customer = get_object_or_404(models.Customer, id=request.POST.get('customer'))
        req.product = get_object_or_404(models.Product, id=request.POST.get('product'))
        req.qty = request.POST['qty']
        req.discount = request.POST['discount']
        req.description = request.POST['description']
        req.save()
        success = 'سفارش جدید ثبت شد ، مشاهده سفارش'
        link = get_object_or_404(models.Order_request, id=req.id)
        context = {'customers': customers , 'products':products, 'success':success, 'link':link}
        return render(request, 'crm/home/order_registration.html', context)

    context = {'customers': customers , 'products':products}
    html_template = loader.get_template('crm/home/order_registration.html')
    return HttpResponse(html_template.render(context, request))








#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def order_edit(request, id):
    req = get_object_or_404(models.Order_request, id=id)
    customers = models.Customer.objects.all().order_by('-date_created')
    products = models.Product.objects.all().order_by('-date_created')
    if request.method=="POST":
        req.user = request.user
        req.customer = get_object_or_404(models.Customer, id=request.POST.get('customer'))
        req.product = get_object_or_404(models.Product, id=request.POST.get('product'))
        req.qty = request.POST['qty']
        req.discount = request.POST['discount']
        req.description = request.POST['description']
        req.status = request.POST['status']
        req.save()
        success = 'ویرایش سفارش ثبت شد ، مشاهده سفارش'
        link = get_object_or_404(models.Order_request, id=req.id)
        context = {'req':req, 'customers': customers , 'products':products, 'success':success, 'link':link}
        return render(request, 'crm/home/order_edit.html', context)

    context = {'req':req, 'customers': customers , 'products':products}
    html_template = loader.get_template('crm/home/order_edit.html')
    return HttpResponse(html_template.render(context, request))









#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def customer_edit(request, id):
    customer = get_object_or_404(models.Customer, id=id)
    products = models.Product.objects.all().order_by('-date_created')

    if request.method=="POST":

        if request.POST.get('substantial'):
            substantial = True
        else:
            substantial = False

        customer.name = request.POST['name']
        customer.phone = request.POST['phone']
        customer.company = request.POST['company']
        customer.address = request.POST['address']
        customer.additional_information = request.POST['additional_information']
        customer.substantial = substantial
        customer.save()

        customer.product_tag.clear()

        get_products = request.POST.getlist('products')
        for product in get_products:
           if Product.objects.all().exists():
              product = Product.objects.get(id=product)
              customer.product_tag.add(product)


        success = 'ویرایش اطلاعات مشتری انجام شد ، مشاهده پروفایل'
        link = get_object_or_404(models.Customer, id=customer.id)

        context = {'customer':customer, 'products':products, 'success':success, 'link':link}
        return render(request, 'crm/home/customer_edit.html', context)

    context = {'customer':customer, 'products':products}
    html_template = loader.get_template('crm/home/customer_edit.html')
    return HttpResponse(html_template.render(context, request))































# End
