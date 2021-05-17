from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Profile
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin




admin.site.site_header= "tttttt"
admin.site.site_title= "ttttt"

admin.site.register(LogEntry)



class ItemAdmin(ImportExportModelAdmin):
    list_display = ('name','short_description','image_tag')
    #list_filter = ("manager", "position")

admin.site.register(models.Item, ItemAdmin)
