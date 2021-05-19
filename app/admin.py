from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Item, City, Neighbourhood, Tags #, Media_center
from import_export import resources
from import_export.admin import ImportExportModelAdmin


admin.site.site_header= "املاک"
admin.site.site_title= "املاک"




admin.site.register(LogEntry)



#------------------------------------------------------------------------------
class TagsAdmin(ImportExportModelAdmin):
    list_display = ('name', 'descriptions')
admin.site.register(models.Tags, TagsAdmin)

'''
#------------------------------------------------------------------------------
class Media_centerAdmin(ImportExportModelAdmin):
    list_display = ('image_tag', 'image_tag')
admin.site.register(models.Media_center, Media_centerAdmin)
'''

#------------------------------------------------------------------------------
class CityAdmin(ImportExportModelAdmin):
    list_display = ('name', 'descriptions')
admin.site.register(models.City, CityAdmin)


#------------------------------------------------------------------------------
class NeighbourhoodAdmin(ImportExportModelAdmin):
    list_display = ('name', 'descriptions')
admin.site.register(models.Neighbourhood, NeighbourhoodAdmin)


#------------------------------------------------------------------------------
class ItemAdmin(ImportExportModelAdmin):
    list_display = ('name', 'area_size', 'city', 'neighbourhood', 'buy_status', 'estate_status', 'building_status', 'parking')
    list_filter = ("city", "neighbourhood", "buy_status", "estate_status", "building_status", "area_size", 'parking', 'elevator' )
    fields = (
        ('buy_status', 'estate_status', 'building_status'),
        ('area_size', 'room_qty', 'building_age'),
        ('parking', 'storage_room', 'elevator', 'balcony', 'remote_door', 'lobby', 'guard', 'pool', 'air_conditioning_system', 'wall_cupboard', 'master_bath', 'toilet'),
        ('deposit', 'rent', 'price'),
        ('city', 'neighbourhood'),
        'image',
        'additional_information',
        'tags'
        )


admin.site.register(models.Item, ItemAdmin)






# End
