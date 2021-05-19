from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
from django.template.defaultfilters import truncatechars




#------------------------------------------------------------------------------
class Tags(models.Model):
    name=models.CharField(max_length=200,verbose_name = "برچسب")
    descriptions = models.TextField(max_length=500,null=True, blank=True,verbose_name = "توضیحات")

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"

    def __str__(self):
        return self.name


#------------------------------------------------------------------------------
class City(models.Model):
    name=models.CharField(max_length=200,verbose_name = "نام")
    descriptions = models.TextField(max_length=500,null=True, blank=True,verbose_name = "توضیحات")

    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهر ها"

    def __str__(self):
        return self.name


#------------------------------------------------------------------------------
class Neighbourhood(models.Model):
    name=models.CharField(max_length=200,verbose_name = "نام")
    descriptions = models.TextField(max_length=500,null=True, blank=True,verbose_name = "توضیحات")

    class Meta:
        verbose_name = "محله"
        verbose_name_plural = "محله ها"

    def __str__(self):
        return self.name





#------------------------------------------------------------------------------
class Item(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CHOICES1 = ( ('اجاره','اجاره'), ('خرید','خرید'), ('رهن','رهن') )
    buy_status = models.CharField(max_length=10,choices=CHOICES1,verbose_name = "وضعیت خرید")
    CHOICES2 = ( ('مسکونی','مسکونی'), ('تجاری','تجاری') )
    estate_status = models.CharField(max_length=15,choices=CHOICES2,verbose_name = "وضعیت ملک")
    CHOICES3 = ( ('ویلایی','ویلایی'), ('اپارتمانی','اپارتمانی') )
    building_status = models.CharField(max_length=10,choices=CHOICES3,verbose_name = "وضعیت ساختمان")
    area_size = models.IntegerField(null=True,blank=True, verbose_name = "متراژ")
    room_qty = models.IntegerField(null=True,blank=True, verbose_name = "تعداد اتاق")
    building_age = models.IntegerField(null=True,blank=True, verbose_name = "سن بنا")
    parking = models.BooleanField(default=True, verbose_name = "پارکینگ" )
    storage_room = models.BooleanField(default=True, verbose_name = "انباری" )
    elevator = models.BooleanField(default=False, verbose_name = "آسانسور" )
    balcony = models.BooleanField(default=False, verbose_name = "بالکن" )
    remote_door = models.BooleanField(default=False, verbose_name = "درب ریموت" )
    lobby = models.BooleanField(default=False, verbose_name = "لابی" )
    guard = models.BooleanField(default=False, verbose_name = "نگهبان" )
    pool = models.BooleanField(default=False, verbose_name = "استخر" )
    air_conditioning_system = models.BooleanField(default=False, verbose_name = "سیستم تهویه" )
    wall_cupboard = models.BooleanField(default=False, verbose_name = "کمد دیواری" )
    master_bath = models.BooleanField(default=False, verbose_name = "حمام مستر" )
    toilet = models.BooleanField(default=False, verbose_name = "توالت فرنگی" )
    deposit = models.IntegerField(null=True,blank=True, verbose_name = "پول پیش")
    rent = models.IntegerField(null=True,blank=True, verbose_name = "اجاره")
    price = models.IntegerField(null=True,blank=True, verbose_name = "قیمت خرید ")
    image1 = models.ImageField(upload_to='media', default='media/Default.png' ,null=True, blank=True ,verbose_name = "1تصویر")
    image2 = models.ImageField(upload_to='media', default='media/Default.png' ,null=True, blank=True ,verbose_name = "2تصویر")
    image3 = models.ImageField(upload_to='media', default='media/Default.png' ,null=True, blank=True ,verbose_name = "3تصویر")
    image4 = models.ImageField(upload_to='media', default='media/Default.png' ,null=True, blank=True ,verbose_name = "4تصویر")
    #image = models.ForeignKey(Media_center, on_delete=models.CASCADE,null=True, blank=True,verbose_name = "تصویر")
    additional_information = models.TextField(max_length=1000,null=True, blank=True,verbose_name = "اطلاعات تکمیلی")
    city = models.ForeignKey(City, on_delete=models.CASCADE,null=True, blank=True,verbose_name = "شهر")
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE,null=True, blank=True,verbose_name = "محله")
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE,null=True, blank=True,verbose_name = "برچسب")
    #location = LocationField(null=True,blank=True)


    class Meta:
        verbose_name = "ملک"
        verbose_name_plural = "املاک"

    def __str__(self):
        return str(self.buy_status +" "+ self.building_status +" "+ self.estate_status +" "+ self.neighbourhood )

    def name(self):
        return str(self.buy_status +" "+ self.building_status +" "+ self.estate_status +" "+ self.neighbourhood )

    def get_absolute_url(self):
        return reverse('app:item_detail',args=[self.id])

    @property
    def short_description(self):
        return truncatechars(self.additional_Information, 70)







# End
