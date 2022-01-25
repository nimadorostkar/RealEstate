import json

from django.contrib import admin
from django.utils import timezone

from pwa_webpush import send_user_notification
from .custom_site_class import CustomSite
from .models import PushInformation, PushMessage
from .utils import _send_notification


@admin.register(PushInformation)
class PushInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "subscription", "group")
    actions = ("send_test_message",)

    def send_test_message(self, request, queryset):
        result = []
        payload = {"head": "Hey", "body": "Hello World"}
        for device in queryset:
            result.append(_send_notification(device, json.dumps(payload), 0))


@admin.register(PushMessage)
class PwaPushMessageAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        site = CustomSite(request)
        obj.save()

        if not obj.sent and obj.active and obj.send_on <= timezone.now():
            payload = {
                "head": obj.title,
                "body": obj.message,
                "icon": site.get_external_url("/static/pwa/icons/apple-icon-72x72.png") if not obj.icon else obj.icon,
                "url": site.get_external_url("/m/") if not obj.url else obj.url,
            }

            if not obj.send_to:
                push_users = PushInformation.objects.all()

            else:
                push_users = PushInformation.objects.filter(user=obj.send_to)

            for push_user in push_users:
                send_user_notification(user=push_user.user, payload=payload, ttl=1000)
                obj.sent = True
                obj.save()

    list_display = (
        u"active",
        u"send_on",
        u"title",
        u"message",
        u"url",
        u"icon",
    )
    list_filter = (u"active", u"send_on")
