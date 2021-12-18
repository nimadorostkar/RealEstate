from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Order_request, Order_incomings
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin
from .actions import export_as_csv_action





'''
#------------------------------------------------------------------------------
class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'phone', 'short_description')
    list_filter = ("substantial", "date_created")
    search_fields = ['name',]
    actions = [export_as_csv_action("CSV خروجی", fields=['id', 'name', 'phone', 'additional_information', 'substantial' ])]


admin.site.register(models.Customer, CustomerAdmin)
'''





#------------------------------------------------------------------------------
class Order_incomingsInline(StackedInlineJalaliMixin, TabularInlineJalaliMixin, admin.TabularInline):
    model = Order_incomings
    extra = 1


class Order_requestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('item','user','customer','short_description','status')
    list_filter = ("user", 'item','status', 'date_created')
    search_fields = ['item']
    raw_id_fields = ('item', 'user', 'customer')
    inlines = [ Order_incomingsInline, ]
    actions = [export_as_csv_action("CSV خروجی", fields=['id','user', 'customer', 'item', 'qty', 'description', 'discount', 'status' ])]



admin.site.register(models.Order_request, Order_requestAdmin)














# End
