from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Profile, Info, Tags, Area, Item, ItemImage
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter, DraggableMPTTAdmin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


admin.site.site_header= " آتروتک "
admin.site.site_title= " Atrotech "
admin.site.register(LogEntry)




#------------------------------------------------------------------------------
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name','phone','address', 'image_tag')
    search_fields = ['user_name', 'phone', 'address']
admin.site.register(models.Profile, ProfileAdmin)







#------------------------------------------------------------------------------
class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1

class ItemAdmin(ImportExportModelAdmin):
    list_display = ('buy_status','estate_status','building_status','area_size','area', 'date')
    list_filter = ("buy_status", "estate_status", "building_status", "date")
    search_fields = ['area', 'area_size', 'additional_information']
    raw_id_fields = ('area', 'tags')
    inlines = [ ItemImageInline, ]

admin.site.register(models.Item, ItemAdmin)
