from django.db import models

# Create your models here.




#------------------------------------------------------------------------------
class Item(models.Model):

        CHOICES1 = ( ('R','Rent'), ('B','Buy'), ('M','Mortgage') )
        CHOICES2 = ( ('R','Residential'), ('C','Commercial') )

    name = models.CharField(max_length=400,verbose_name = "نام")
    buy_status = models.CharField(max_length=1,choices=CHOICES1,verbose_name = "وضعیت خرید")
    estate_status = models.CharField(max_length=1,choices=CHOICES2,verbose_name = "وضعیت ملک")
    area_size = models.IntegerField(null=True,blank=True, verbose_name = "متراژ")
    roomـqty = models.IntegerField(null=True,blank=True, verbose_name = "تعداد اتاق")
    parking = models.BooleanField(default=True, verbose_name = "پارکینگ" )
    storage_room = models.BooleanField(default=True, verbose_name = "انباری" )

    description=models.TextField(max_length=1000,null=True, blank=True,verbose_name = "مشخصات")
    min_inventory = models.IntegerField(null=True,blank=True, verbose_name = " حداقل موجودی ")
    manager = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True,verbose_name = "مسئول")
    supplier = models.CharField(max_length=300,null=True, blank=True,verbose_name = "تامین کننده")
    pro_cap_day = models.IntegerField(default='1', null=True,blank=True, verbose_name = " ظرفیت تولید در روز ")
    percent_error = models.IntegerField(default='1', null=True,blank=True, verbose_name = " درصد خطا ")
    #location = LocationField(null=True,blank=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']

    class Meta:
        verbose_name = "فرآیند"
        verbose_name_plural = " فرآیند ها "

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app:processes_detail',args=[self.id])

    @property
    def short_description(self):
        return truncatechars(self.description, 70)
