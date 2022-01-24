from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.db.models.base import Model
from django.db.models.signals import pre_save
from core.utils import unique_slug_generator
from extensions.utils import jalali_converter







#------------------------------------------------------------------------------
class PostComment(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def j_create_at(self):
        return jalali_converter(self.create_at)

    def __str__(self):
        return f'{self.sender.get_username()}'

    class Meta:
      verbose_name = "نظر"
      verbose_name_plural = "نظرات"





#------------------------------------------------------------------------------
class Categories(models.Model):
    categoryname = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, verbose_name="نشانی پیوند (link)")


    def __str__(self):
        return self.categoryname

    class Meta:
      verbose_name = "دسته بندی"
      verbose_name_plural = "دسته بندی ها"





#------------------------------------------------------------------------------
class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = models.SlugField(max_length=255, null=True, blank=True, verbose_name="نشانی پیوند (link)")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نویسنده")
    img = models.ImageField(upload_to='blog', null=True, verbose_name="تصویر")
    body = RichTextField(blank=False, null=True, verbose_name="متن")
    comments = models.ManyToManyField(PostComment, blank=True, verbose_name="نظرات")
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, null=True, on_delete=models.PROTECT, related_name='category_set', verbose_name="دسته بندی")

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def j_post_date(self):
        return jalali_converter(self.post_date)

    class Meta:
      verbose_name = "پست"
      verbose_name_plural = "پست ها"

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)








# End
