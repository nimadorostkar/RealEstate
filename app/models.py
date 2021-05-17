from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
from django.template.defaultfilters import truncatechars





#------------------------------------------------------------------------------
class Item(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, k=5)
    CHOICES1 = ( ('اجاره','Rent'), ('خرید','Buy'), ('رهن','Mortgage') )
    buy_status = models.CharField(max_length=10,choices=CHOICES1,verbose_name = "وضعیت خرید")
    CHOICES2 = ( ('مسکونی','Residential'), ('تجاری','Commercial') )
    estate_status = models.CharField(max_length=15,choices=CHOICES2,verbose_name = "وضعیت ملک")
    CHOICES3 = ( ('ویلایی','Villa'), ('اپارتمانی','Apartment') )
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
    image = models.ImageField(upload_to='media', default='media/Default.png' ,null=True, blank=True,verbose_name = "تصویر")
    additional_information = models.TextField(max_length=1000,null=True, blank=True,verbose_name = "اطلاعات تکمیلی")
    city = models.CharField(max_length=50,null=True, blank=True,verbose_name = "شهر")
    neighbourhood = models.CharField(max_length=50,null=True, blank=True,verbose_name = "محله")
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

    def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.image.url))

    @property
    def short_description(self):
        return truncatechars(self.additional_Information, 70)







# End
