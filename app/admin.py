from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Item
from import_export import resources
from import_export.admin import ImportExportModelAdmin




admin.site.site_header= "املاک"
admin.site.site_title= "املاک"

admin.site.register(LogEntry)



class ItemAdmin(ImportExportModelAdmin):
    list_display = ('name', 'area_size', 'city', 'neighbourhood', 'buy_status', 'estate_status', 'building_status', 'parking', 'image_tag')
    list_filter = ("city", "neighbourhood", "buy_status", "estate_status", "building_status", "area_size", 'parking' )

    fields = (
        ('buy_status', 'estate_status', 'building_status'),
        ('area_size', 'roomـqty', 'building_age'),
        ('parking', 'storage_room', 'elevator', 'balcony'),
        ('deposit', 'Rent', 'price'),
        ('city', 'neighbourhood'),
        'image',
        'additional_Information'
    )

admin.site.register(models.Item, ItemAdmin)
