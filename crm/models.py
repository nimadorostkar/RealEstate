from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.template.defaultfilters import truncatechars
from django_jalali.db import models as jmodels
from datetime import datetime




#------------------------------------------------------------------------------
class Product(models.Model):
    available = models.BooleanField(default=True, verbose_name = "موجود" )
    name = models.CharField(max_length=200, unique=True, verbose_name = "نام")
    inventory = models.IntegerField(default='1', verbose_name = "موجودی")
    price = models.IntegerField( verbose_name = "قیمت ( ریال )")
    description = models.TextField(max_length=5000,null=True, blank=True,verbose_name = "توضیحات")
    image = models.ImageField(upload_to='media', default='media/Default.png', verbose_name = "تصویر")
    date_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ")

    def __str__(self):
        return self.name

    def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.image.url))

    def get_absolute_url(self):
        return reverse('product_detail',args=[self.id])

    @property
    def short_description(self):
        return truncatechars(self.description, 70)

    @property
    def price_display(self):
        return "%s ریال " % self.price

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"







#------------------------------------------------------------------------------
class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name = "نام")
    phone = models.CharField(max_length=200, blank=True, null=True, verbose_name = "تلفن")
    company = models.CharField(max_length=200, blank=True, null=True, verbose_name = "نام شرکت")
    address = models.CharField(max_length=400, blank=True, null=True, verbose_name = "آدرس")
    additional_information = models.TextField(max_length=1000,null=True, blank=True,verbose_name = "اطلاعات تکمیلی")
    substantial = models.BooleanField(default=False, verbose_name = "مشتری ویژه" )
    product_tag = models.ManyToManyField(Product, blank=True, verbose_name = "تگ محصولی")
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
    product = models.ForeignKey(Product ,on_delete=models.CASCADE, verbose_name = "محصول")
    qty = models.IntegerField(default='1', verbose_name = "تعداد" )
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name = "توضیحات")
    discount = models.IntegerField(default='0', verbose_name = "درصد تخفیف" )
    CHOICES = ( ('تکمیل شده','تکمیل شده'), ('لغو شده','لغو شده'), ('دریافت پیش پرداخت','دریافت پیش پرداخت'), ('در حال بررسی','در حال بررسی'), ('جدید','جدید'))
    status = models.CharField(max_length=30,choices=CHOICES, default='جدید', verbose_name = "وضعیت")
    date_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ")
    date_updated = jmodels.jDateTimeField(auto_now=True, verbose_name = "آخرین ویرایش")


    def __str__(self):
        return  " سفارش " + self.product.name + ' برای ' + self.customer.name

    @property
    def short_description(self):
        return truncatechars(self.description, 70)

    def get_absolute_url(self):
        return reverse('order_req_detail',args=[self.id])

    def get_absolute_edit_url(self):
        return reverse('order_edit',args=[self.id])

    def get_absolute_invoice_url(self):
        return reverse('order_invoice',args=[self.id])

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"



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
