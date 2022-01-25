from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Profile, Area, Item, ItemImage, Slider, Fav, Contact, Ownership, Settings
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


admin.site.site_header= " دستیار املاک "
admin.site.site_title= "  دستیار املاک  "
admin.site.register(LogEntry)







#------------------------------------------------------------------------------
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'title')
admin.site.register(models.Settings, SettingsAdmin)








#------------------------------------------------------------------------------
class ProfileAdmin(ImportExportModelAdmin):
    list_display = ('image_tag', 'user_type', 'user_name','phone','sales_expert')
    list_filter = ('user_type', "date_created")
    search_fields = ['user_name', 'phone']
admin.site.register(models.Profile, ProfileAdmin)











#------------------------------------------------------------------------------
class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1

class ItemAdmin(ModelAdminJalaliMixin,ImportExportModelAdmin):
    list_display = ('image_tag', 'buy_status', 'estate_status', 'area_size', 'area', 'date', 'available')
    list_filter = ('available',"buy_status", "estate_status", "date")
    search_fields = ['additional_information']
    raw_id_fields = ('area',)
    inlines = [ ItemImageInline, ]


admin.site.register(models.Item, ItemAdmin)






#------------------------------------------------------------------------------
class AreaAdmin(ImportExportModelAdmin):
    list_display = ('name','name')
    search_fields = ['name']

admin.site.register(models.Area, AreaAdmin)






#------------------------------------------------------------------------------
class OwnershipAdmin(ImportExportModelAdmin):
    list_display = ('name','phone')
    search_fields = ['name']

admin.site.register(models.Ownership, OwnershipAdmin)





#------------------------------------------------------------------------------
class SliderAdmin(ImportExportModelAdmin):
    list_display = ('Image','image_tag')

admin.site.register(models.Slider, SliderAdmin)





#------------------------------------------------------------------------------
class FavAdmin(ImportExportModelAdmin):
    list_display = ('user','item')
    list_filter = ("user", "item")

admin.site.register(models.Fav, FavAdmin)





#------------------------------------------------------------------------------
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'j_created_on')
    list_filter = ('name', 'created_on')
    search_fields = ('name', 'phone', 'body')

admin.site.register(Contact, ContactAdmin)












#End
