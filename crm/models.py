from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.template.defaultfilters import truncatechars
from django_jalali.db import models as jmodels
from datetime import datetime
from app.models import Item





#------------------------------------------------------------------------------
class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name = "نام")
    phone = models.CharField(max_length=200, blank=True, null=True, verbose_name = "تلفن")
    additional_information = models.TextField(max_length=1000,null=True, blank=True,verbose_name = "اطلاعات تکمیلی")
    substantial = models.BooleanField(default=False, verbose_name = "مشتری ویژه" )
    item = models.ForeignKey(Item , blank=True, null=True, on_delete=models.CASCADE, verbose_name = "فابل")
    date_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('customer_detail',args=[self.id])

    def get_absolute_edit_url(self):
        return reverse('customer_edit',args=[self.id])

    @property
    def short_description(self):
        return truncatechars(self.additional_information, 70)

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"










#------------------------------------------------------------------------------
class Order_request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name = "کارشناس فروش")
    customer = models.ForeignKey(Customer ,on_delete=models.CASCADE, verbose_name = "خریدار")
    item = models.ForeignKey(Item ,on_delete=models.CASCADE, verbose_name = "فایل")
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name = "توضیحات")
    CHOICES = ( ('تکمیل شده','تکمیل شده'), ('لغو شده','لغو شده'), ('دریافت پیش پرداخت','دریافت پیش پرداخت'), ('در حال بررسی','در حال بررسی'), ('جدید','جدید'))
    status = models.CharField(max_length=30,choices=CHOICES, default='جدید', verbose_name = "وضعیت")
    date_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ")
    date_updated = jmodels.jDateTimeField(auto_now=True, verbose_name = "آخرین ویرایش")


    def __str__(self):
        return  " درخواست " + str(self.item) + ' برای ' + self.customer.name

    @property
    def short_description(self):
        return truncatechars(self.description, 70)

    def get_absolute_url(self):
        return reverse('order_req_detail',args=[self.id])

    def get_absolute_edit_url(self):
        return reverse('order_edit',args=[self.id])

    class Meta:
        verbose_name = "درخواست خرید"
        verbose_name_plural = "درخواست های خرید"



class Order_incomings(models.Model):
    request = models.ForeignKey(Order_request ,on_delete=models.CASCADE, verbose_name = "برای سفارش")
    amount = models.IntegerField( verbose_name = "قیمت ( ریال )")
    date_created = jmodels.jDateField(verbose_name = "تاریخ")


    def __str__(self):
      return " مبلغ " + str(self.amount) + " برای " + str(self.request) + " در تاریخ " + str(self.date_created)

    class Meta:
        verbose_name = "مبلغ ورودی سفارش"
        verbose_name_plural = "مبالغ ورودی سفارش"





















# End
