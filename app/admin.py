from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Profile, Tags, Area, Item, ItemImage, Slider, Favorite
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

class ItemAdmin(ModelAdminJalaliMixin,ImportExportModelAdmin):
    list_display = ('buy_status','estate_status','building_status','area_size','area', 'date', 'image_tag')
    list_filter = ("buy_status", "estate_status", "building_status", "date")
    search_fields = ['area', 'area_size', 'additional_information']
    raw_id_fields = ('area', 'tags')
    inlines = [ ItemImageInline, ]


admin.site.register(models.Item, ItemAdmin)








#------------------------------------------------------------------------------
class TagsAdmin(ImportExportModelAdmin):
    list_display = ('name','name')
    search_fields = ['name']

admin.site.register(models.Tags, TagsAdmin)






#------------------------------------------------------------------------------
class AreaMPTTModelAdmin(ImportExportMixin, MPTTModelAdmin, TreeRelatedFieldListFilter):
    mptt_level_indent = 15

admin.site.register(Area, DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title'),
    list_display_links=('indented_title',),)







#------------------------------------------------------------------------------
class SliderAdmin(ImportExportModelAdmin):
    list_display = ('Image','Image')

admin.site.register(models.Slider, SliderAdmin)







#End
