from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatechars






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





#------------------------------------------------------------------------------
class Rom(models.Model):
    name = models.CharField(max_length=40, default='device name')
    UUID = models.CharField(max_length=20)
    family_id = models.CharField(max_length=20)
    node_id = models.CharField(max_length=20)
    updated_on = models.DateTimeField(auto_now= True)
    created_on = models.DateTimeField()

    def __str__(self):
        return self.UUID

    def get_absolute_url(self):
        return reverse('app:nodes_detail',args=[self.id])

    def get_absolute_sensor_url(self):
        return reverse('app:sensors_detail',args=[self.id])



#------------------------------------------------------------------------------
class Node1(models.Model):
    UUID = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    tamper = models.CharField(max_length=20)
    moves = models.CharField(max_length=20)
    resets = models.CharField(max_length=20)
    charger = models.CharField(max_length=20)
    USB = models.CharField(max_length=20)
    HMI = models.CharField(max_length=20)
    cpuTemp = models.CharField(max_length=20)
    created_on = models.DateTimeField()

    def __str__(self):
        return self.UUID



#------------------------------------------------------------------------------
class Temp12(models.Model):
    UUID = models.CharField(max_length=20)
    temp = models.CharField(max_length=20)
    created_on = models.DateTimeField()

    def __str__(self):
        return self.UUID

    class Meta:
        verbose_name = " سنسور دما Temp12 "
        verbose_name_plural = " سنسور های دما  Temp12 "

    def windowsize(self):
        if self.temp > 40:
            return False
        else:
            return True




#------------------------------------------------------------------------------
class Gps2(models.Model):
    UUID = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    created_on = models.DateTimeField()

    def __str__(self):
        return self.UUID



#------------------------------------------------------------------------------
class Sd1(models.Model):
    UUID = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    period = models.CharField(max_length=20)
    capacity = models.CharField(max_length=20)
    free = models.CharField(max_length=20)
    cycles = models.CharField(max_length=20)
    created_on = models.DateTimeField()

    def __str__(self):
        return self.UUID



#------------------------------------------------------------------------------
class Modem1(models.Model):
    UUID = models.CharField(max_length=20)
    rssi = models.CharField(max_length=20)
    battery = models.CharField(max_length=20)
    updaterate = models.CharField(max_length=20)
    sent = models.CharField(max_length=20)
    lost = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    created_on = models.DateTimeField()

    def __str__(self):
        return self.UUID





#------------------------------------------------------------------------------
class User_uuid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    UUID = models.CharField(max_length=20)


    def __str__(self):
        return str(self.user)










# End
