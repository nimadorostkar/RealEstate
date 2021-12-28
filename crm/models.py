from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.template.defaultfilters import truncatechars
from django_jalali.db import models as jmodels
from datetime import datetime
from app.models import Item, Profile







#------------------------------------------------------------------------------
class Order_request(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_profile', verbose_name = "کارشناس فروش")
    customer = models.ForeignKey(Profile ,on_delete=models.CASCADE, related_name='customer_profile', verbose_name = "خریدار")
    item = models.ForeignKey(Item ,on_delete=models.CASCADE, verbose_name = "فایل")
    final_price = models.CharField(max_length=200, default='نامشخص' ,verbose_name = "قیمت نهایی")
    prepayment = models.CharField(max_length=200, default='نامشخص' , verbose_name = "بیعانه")
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name = "توضیحات")
    CHOICES = ( ('تکمیل شده','تکمیل شده'), ('لغو شده','لغو شده'), ('دریافت پیش پرداخت','دریافت پیش پرداخت'), ('در حال بررسی','در حال بررسی'), ('جدید','جدید'))
    status = models.CharField(max_length=30,choices=CHOICES, default='جدید', verbose_name = "وضعیت")
    date_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ")
    date_updated = jmodels.jDateTimeField(auto_now=True, verbose_name = "آخرین ویرایش")


    def __str__(self):
        return  " درخواست " + str(self.item) + ' برای ' + self.customer.user.first_name +' '+ self.customer.user.last_name

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
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,verbose_name = "کارشناس فروش")
    description = models.CharField(max_length=200 , verbose_name = "توضیحات")
    date_created = jmodels.jDateTimeField(verbose_name = "تاریخ")


    def __str__(self):
      return str(self.date_created)

    class Meta:
        verbose_name = "پیگیری"
        verbose_name_plural = "پیگیری ها"

    #def get_absolute_edit_url(self):
        #return reverse('incomings_edit',args=[self.id])





















# End
