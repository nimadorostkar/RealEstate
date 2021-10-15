from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatechars
from mptt.models import MPTTModel, TreeForeignKey





#------------------------------------------------------------------------------
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True,related_name='profile',verbose_name = "کاربر")
  phone = models.CharField(max_length=50,null=True, blank=True,verbose_name = " شماره تماس  ")
  address = models.CharField(max_length=3000,null=True, blank=True,verbose_name = " آدرس  ")
  user_photo = models.ImageField(default='default.png', upload_to='profile_pics', null=True, blank=True, verbose_name = "تصویر")


  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
      if created:
          Profile.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
      instance.profile.save()

  def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.user_photo.url))

  def user_name(self):
        return str(self.user)

  class Meta:
      verbose_name = "پروفایل"
      verbose_name_plural = " پروفایل ها "

  def __str__(self):
    return "پروفایل : " + str(self.user)







'''
#------------------------------------------------------------------------------
class Info(models.Model):
    logo = models.ImageField(upload_to='media', default='media/logo.png' ,null=True, blank=True ,verbose_name = "لوگو ")
    name = models.CharField(max_length=200,null=True, blank=True,verbose_name = "نام")
    descriptions = models.TextField(max_length=500,null=True, blank=True,verbose_name = "توضیحات")
    phone = models.CharField(max_length=200,null=True, blank=True,verbose_name = "تلفن")
    email = models.CharField(max_length=200,null=True, blank=True,verbose_name = "ایمیل")
    manager = models.CharField(max_length=200,null=True, blank=True,verbose_name = "مدیر")
    address = models.CharField(max_length=200,null=True, blank=True,verbose_name = "آدرس")
    instagram = models.CharField(max_length=200,null=True, blank=True,verbose_name = "instagram")
    twitter = models.CharField(max_length=200,null=True, blank=True,verbose_name = "twitter")
    telegram = models.CharField(max_length=200,null=True, blank=True,verbose_name = "telegram")
    whatsapp = models.CharField(max_length=200,null=True, blank=True,verbose_name = "whatsapp")


    class Meta:
        verbose_name = "اطلاعات"
        verbose_name_plural = "اطلاعات"

    def __str__(self):
        return self.name
'''




#------------------------------------------------------------------------------
class Tags(models.Model):
    name=models.CharField(max_length=200,verbose_name = "برچسب")

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"

    def __str__(self):
        return self.name







#------------------------------------------------------------------------------
class Area(MPTTModel):
    name = models.CharField(max_length=200, unique=True, verbose_name = "نام")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',verbose_name = "والد")

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "منطقه"
        verbose_name_plural = "مناطق"

    #def get_absolute_url(self):
        #return reverse('app:category_detail',args=[self.id])

    def __unicode__(self):
        return u"%s" % (self.name)

    def __str__(self):
        return str(self.name)





#------------------------------------------------------------------------------
class Item(models.Model):
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
    deposit = models.IntegerField(null=True,blank=True, default='0', verbose_name = "پول پیش")
    rent = models.IntegerField(null=True,blank=True, default='0', verbose_name = "اجاره")
    price = models.IntegerField(null=True,blank=True, default='0', verbose_name = "قیمت خرید ")
    area = models.ForeignKey(Area, on_delete=models.CASCADE,null=True, blank=True,verbose_name = "منطقه")
    tags = models.ManyToManyField(Tags, blank=True,verbose_name = "برچسب")
    additional_information = models.TextField(max_length=1000,null=True, blank=True,verbose_name = "اطلاعات تکمیلی")
    date = models.DateField(null=True, blank=True, verbose_name = "تاریخ آگهی")
    image = models.ImageField(upload_to='media', default='media/Default.png', null=True, blank=True, verbose_name = "تصویر")
    # video
    # active or not

    class Meta:
        verbose_name = "ملک"
        verbose_name_plural = "املاک"

    def __str__(self):
        return str(self.buy_status +" "+ self.building_status +" "+ self.estate_status +" "+ self.area.name )

    def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.image.url))

    def get_absolute_url(self):
        return reverse('app:items_detail',args=[self.id])

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    Image = models.ImageField(upload_to='media', default='media/Default.png', null=True, blank=True, verbose_name = "تصویر")

    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"








#------------------------------------------------------------------------------
class Slider(models.Model):
    Image = models.ImageField(upload_to='media', default='media/Default.png', null=True, blank=True, verbose_name = "تصویر")

    def __str__(self):
        return "اسلایدر " + str(self.id)

    class Meta:
        verbose_name = "اسلایر"
        verbose_name_plural = "اسلایر ها"






#------------------------------------------------------------------------------
class Fav(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name = "کاربر")
    item = models.ForeignKey(Item, on_delete=models.CASCADE,verbose_name = "آیتم")

    class Meta:
        verbose_name = "مورد علاقه"
        verbose_name_plural = "مورد علاقه ها"

    def __str__(self):
        return self.user.username+'-'+str(self.item.id)







#------------------------------------------------------------------------------
class Call_request(models.Model):
    phone_number = models.CharField(max_length=20 , verbose_name = "شماره تلفن")

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "درخواست تماس"
        verbose_name_plural = "درخواست های تماس"








# End
