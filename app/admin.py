from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Item
from import_export import resources
from import_export.admin import ImportExportModelAdmin




admin.site.site_header= "tttttt"
admin.site.site_title= "ttttt"

admin.site.register(LogEntry)



class ItemAdmin(ImportExportModelAdmin):
    list_display = ('name', 'area_size', 'city', 'neighbourhood', 'buy_status', 'estate_status', 'building_status', 'image_tag')
    list_filter = ("city", "neighbourhood", "buy_status", "estate_status", "building_status", "area_size", )

admin.site.register(models.Item, ItemAdmin)
