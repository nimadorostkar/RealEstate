from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Customer, Order_request, Order_incomings
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin
from .actions import export_as_csv_action






#------------------------------------------------------------------------------
class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'phone', 'short_description')
    list_filter = ("substantial", "date_created", "item")
    search_fields = ['name',]
    raw_id_fields = ('item',)
    actions = [export_as_csv_action("CSV خروجی", fields=['id', 'name', 'phone', 'additional_information', "item", 'substantial' ])]


admin.site.register(models.Customer, CustomerAdmin)






#------------------------------------------------------------------------------
class Order_incomingsInline(StackedInlineJalaliMixin, TabularInlineJalaliMixin, admin.TabularInline):
    model = Order_incomings
    extra = 1


class Order_requestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('product','user','customer','short_description','status')
    list_filter = ("user", 'product','status', 'date_created')
    search_fields = ['product__name']
    raw_id_fields = ('product', 'user', 'customer')
    inlines = [ Order_incomingsInline, ]
    actions = [export_as_csv_action("CSV خروجی", fields=['id','user', 'customer', 'product', 'qty', 'description', 'discount', 'status' ])]



admin.site.register(models.Order_request, Order_requestAdmin)














# End
