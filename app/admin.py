from django.contrib import admin
from . import models
from .models import Rom, Node1, Temp12, Gps2, Sd1, Modem1, Profile, User_uuid





#------------------------------------------------------------------------------
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name','phone','address', 'image_tag')
    search_fields = ['user_name', 'phone', 'address']
admin.site.register(models.Profile, ProfileAdmin)

#------------------------------------------------------------------------------
class User_uuidAdmin(admin.ModelAdmin):
    list_display = ('user', 'UUID')
admin.site.register(models.User_uuid, User_uuidAdmin)

#------------------------------------------------------------------------------
class RomAdmin(admin.ModelAdmin):
    list_display = ('name', 'UUID', 'family_id', 'node_id', 'created_on', 'id')
admin.site.register(models.Rom, RomAdmin)

#------------------------------------------------------------------------------
class Node1Admin(admin.ModelAdmin):
    list_display = ('UUID', 'status', 'tamper', 'moves', 'resets', 'charger', 'USB', 'HMI', 'cpuTemp')
admin.site.register(models.Node1, Node1Admin)

#------------------------------------------------------------------------------
class Temp12Admin(admin.ModelAdmin):
    list_display = ('UUID', 'temp', 'created_on')
    list_filter = ('UUID','created_on')
admin.site.register(models.Temp12, Temp12Admin)

#------------------------------------------------------------------------------
class Gps2Admin(admin.ModelAdmin):
    list_display = ('UUID', 'latitude', 'longitude', 'created_on')
admin.site.register(models.Gps2, Gps2Admin)

#------------------------------------------------------------------------------
class Sd1Admin(admin.ModelAdmin):
    list_display = ('UUID', 'type', 'period', 'capacity', 'free', 'cycles', 'created_on')
admin.site.register(models.Sd1, Sd1Admin)

#------------------------------------------------------------------------------
class Modem1Admin(admin.ModelAdmin):
    list_display = ('UUID', 'rssi', 'battery', 'updaterate', 'sent', 'lost', 'status', 'created_on')
admin.site.register(models.Modem1, Modem1Admin)
