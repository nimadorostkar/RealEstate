from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatechars
from extensions.utils import jalali_converter
from django.template.defaultfilters import truncatechars
from django_jalali.db import models as jmodels









#------------------------------------------------------------------------------
class Settings(models.Model):
  title = models.CharField(max_length=100, verbose_name = "عنوان")
  title_below = models.CharField(max_length=300 , null=True, blank=True , verbose_name = "متن زیر عنوان")
  introduction_text = models.TextField(max_length=2000 , null=True, blank=True , verbose_name = "متن معرفی" )
  contact_page_text = models.TextField(max_length=2000 , null=True, blank=True , verbose_name = "متن صفحه تماس با ما")
  experts_number = models.IntegerField(default='1', verbose_name = "تعداد کارشناسان")
  email = models.EmailField(max_length=200 , null=True , blank=True , verbose_name = "ایمیل")
  address = models.CharField(max_length=300 , null=True , blank=True , verbose_name = "آدرس")
  phone1 = models.CharField(max_length=20 , null=True , blank=True , verbose_name = "تلفن ۱")
  phone2 = models.CharField(max_length=20 , null=True , blank=True , verbose_name = "تلفن ۲")
  whatsapp_number = models.CharField(max_length=20 , null=True , blank=True , verbose_name = "شماره واتساپ")
  instagram = models.URLField(max_length=500, null=True, blank=True, verbose_name = "لینک اینستاگرام")
  telegram = models.URLField(max_length=500, null=True, blank=True, verbose_name = "لینک تلگرام")
  twitter = models.URLField(max_length=500, null=True, blank=True, verbose_name = "لینک توییتر")
  whatsapp = models.URLField(max_length=500, null=True, blank=True, verbose_name = "لینک واتس اپ")
  lat_long = models.CharField(max_length=50 , null=True , blank=True , verbose_name = "lat & long")
  logo = models.ImageField(default='logo.png', upload_to='logo', null=True, blank=True, verbose_name = "لوگو")
  header_image = models.ImageField(default='header.png', upload_to='header', null=True, blank=True, verbose_name = "تصویر سربرگ (header)")

  def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.logo.url))

  class Meta:
      verbose_name = "تنظیمات"
      verbose_name_plural = "تنظیمات"

  def __str__(self):
    return self.title











#------------------------------------------------------------------------------
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True,related_name='profile',verbose_name = "کاربر")
  phone = models.CharField(max_length=50,null=True, blank=True,verbose_name = " شماره تماس  ")
  additional_information = models.TextField(max_length=1000,null=True, blank=True,verbose_name = "اطلاعات تکمیلی")
  user_photo = models.ImageField(default='default.png', upload_to='profile_pics', null=True, blank=True, verbose_name = "تصویر")
  CHOICES = ( ('کاربر','کاربر'), ('کاربر ویژه','کاربر ویژه'), ('کارشناس','کارشناس'), ('مدیر','مدیر') )
  user_type = models.CharField(max_length=30,choices=CHOICES, default='کاربر', verbose_name = "نوع کاربر")
  sales_expert = models.ForeignKey("Profile", null=True, blank=True, on_delete=models.CASCADE,verbose_name = "کارشناس مربوطه")
  date_created = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ ایجاد")


  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
      if created:
          Profile.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
      instance.profile.save()

  def get_absolute_url(self):
      return reverse('customer_detail',args=[self.id])

  def get_absolute_edit_url(self):
      return reverse('customer_edit',args=[self.id])


  def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.user_photo.url))

  @property
  def short_description(self):
      return truncatechars(self.additional_information, 50)


  def user_name(self):
        return str(self.user)

  class Meta:
      verbose_name = "کاربر"
      verbose_name_plural = "کاربران"

  def __str__(self):
    return self.user_type +"|"+ str(self.user)












#------------------------------------------------------------------------------
class Area(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name = "نام")

    class Meta:
        verbose_name = "منطقه"
        verbose_name_plural = "مناطق"

    def __str__(self):
        return str(self.name)







#------------------------------------------------------------------------------
class Ownership(models.Model):
    name = models.CharField(max_length=200,null=True, blank=True,verbose_name = "نام")
    phone = models.CharField(max_length=50,null=True, blank=True,verbose_name = " شماره تماس")

    class Meta:
        verbose_name = "مالکیت"
        verbose_name_plural = "مالکیت ها"

    def __str__(self):
        return str(self.name)






#------------------------------------------------------------------------------
class Item(models.Model):
    available = models.BooleanField(default=True, verbose_name = "قابل مشاهده در سایت" )
    code = models.CharField(max_length=200, unique=True, verbose_name = "کد فایل")
    CHOICES1 = ( ('رهن و اجاره','رهن و اجاره'), ('رهن کامل','رهن کامل'), ('فروش','فروش'), ('پیش فروش','پیش فروش') )
    buy_status = models.CharField(max_length=30,choices=CHOICES1,verbose_name = "نوع معامله")
    CHOICES2 = ( ('آپارتمان','آپارتمان'), ('خانه ویلایی','خانه ویلایی'), ('زمین','زمین'), ('مغازه و تجاری','مغازه و تجاری'), ('دفتر کار اداری','دفتر کار اداری'), ('کلنگی','کلنگی'), ('ویلا','ویلا'), ('باغ','باغ') )
    estate_status = models.CharField(max_length=30,choices=CHOICES2,verbose_name = "نوع ملک")
    area_size = models.IntegerField(null=True,blank=True, verbose_name = "متراژ (متر)")
    room_qty = models.IntegerField(null=True,blank=True, verbose_name = "تعداد اتاق")
    building_age = models.IntegerField(null=True,blank=True, verbose_name = "سن بنا (سال)")
    parking = models.BooleanField(default=False, verbose_name = "پارکینگ" )
    storage_room = models.BooleanField(default=False, verbose_name = "انباری" )
    elevator = models.BooleanField(default=False, verbose_name = "آسانسور" )
    balcony = models.BooleanField(default=False, verbose_name = "بالکن" )
    deposit = models.IntegerField(null=True,blank=True, default='0', verbose_name = "ودیعه (تومان)")
    rent = models.IntegerField(null=True,blank=True, default='0', verbose_name = "اجاره (تومان)")
    price = models.IntegerField(null=True,blank=True, default='0', verbose_name = "قیمت فروش (تومان)")
    area = models.ForeignKey(Area, on_delete=models.CASCADE,verbose_name = "منطقه")
    additional_information = models.TextField(max_length=2000,null=True, blank=True,verbose_name = "اطلاعات تکمیلی")
    date = jmodels.jDateTimeField(auto_now_add=True, verbose_name = "تاریخ آگهی")
    image = models.ImageField(upload_to='media', default='media/Default.png', null=True, blank=True, verbose_name = "تصویر")
    video_link = models.URLField(max_length=500, null=True, blank=True, verbose_name = "لینک ویدئو")
    sales_expert = models.ForeignKey(User, null=True,blank=True, on_delete=models.CASCADE,verbose_name = "کارشناس فروش")
    ownership = models.ForeignKey(Ownership, null=True,blank=True, on_delete=models.CASCADE,verbose_name = "مالکیت")


    class Meta:
        verbose_name = "ملک"
        verbose_name_plural = "املاک"

    def __str__(self):
        return str(self.buy_status +" "+ self.estate_status +" در "+ self.area.name )

    def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.image.url))

    def get_absolute_url(self):
        return reverse('app:items_detail',args=[self.id])

    def get_absolute_crm_url(self):
        return reverse('crm_items_detail',args=[self.id])

    def get_absolute_edit_url(self):
        return reverse('crm_item_edit',args=[self.id])

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    Image = models.ImageField(upload_to='media', default='media/Default.png', null=True, blank=True, verbose_name = "تصویر")

    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"








#------------------------------------------------------------------------------
class Slider(models.Model):
    Image = models.ImageField(upload_to='media', default='media/Default.png', null=True, blank=True, verbose_name = "تصویر")

    def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.Image.url))

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
class Contact(models.Model):
    name = models.CharField(max_length=80, verbose_name="نام")
    phone = models.CharField(max_length=50,verbose_name = " شماره تماس  ")
    body = models.TextField(verbose_name="متن پیام")
    CHOICES = ( ('جدید','جدید'), ('برسی شده','برسی شده') )
    status = models.CharField(max_length=30,choices=CHOICES, default='جدید', verbose_name = "وضعیت")
    created_on = models.DateTimeField(auto_now_add=True)

    def j_created_on(self):
        return jalali_converter(self.created_on)

    def get_absolute_url(self):
        return reverse('contact_detail',args=[self.id])

    class Meta:
      verbose_name = "تماس"
      verbose_name_plural = "تماس ها"

    def __str__(self):
        return str(self.name)





# End
