from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Item, City, Neighbourhood
from import_export import resources
from import_export.admin import ImportExportModelAdmin


admin.site.site_header= "املاک"
admin.site.site_title= "املاک"




admin.site.register(LogEntry)



class CityAdmin(ImportExportModelAdmin):
    list_display = ('name', 'name')
admin.site.register(models.City, CityAdmin)



class NeighbourhoodAdmin(ImportExportModelAdmin):
    list_display = ('name', 'name')
admin.site.register(models.Neighbourhood, NeighbourhoodAdmin)



class ItemAdmin(ImportExportModelAdmin):
    list_display = ('name', 'area_size', 'city', 'neighbourhood', 'buy_status', 'estate_status', 'building_status', 'parking', 'image_tag')
    list_filter = ("city", "neighbourhood", "buy_status", "estate_status", "building_status", "area_size", 'parking', 'elevator' )
    fields = (
        ('buy_status', 'estate_status', 'building_status'),
        ('area_size', 'room_qty', 'building_age'),
        ('parking', 'storage_room', 'elevator', 'balcony', 'remote_door', 'lobby', 'guard', 'pool', 'air_conditioning_system', 'wall_cupboard', 'master_bath', 'toilet'),
        ('deposit', 'rent', 'price'),
        ('city', 'neighbourhood'),
        'image',
        'additional_information'
        )
admin.site.register(models.Item, ItemAdmin)
