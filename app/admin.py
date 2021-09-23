from django.contrib import admin
from . import models
from .models import Profile



#------------------------------------------------------------------------------
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name','phone','address', 'image_tag')
    search_fields = ['user_name', 'phone', 'address']
admin.site.register(models.Profile, ProfileAdmin)
