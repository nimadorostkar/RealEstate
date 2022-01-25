from django.urls import path

from .views import manifest, offline, ServiceWorkerView, save_info

# Serve up serviceworker.js and manifest.json at the root
urlpatterns = [
    path("serviceworker.js", ServiceWorkerView.as_view(), name="serviceworker"),
    path("manifest.json", manifest, name="manifest"),
    path("offline/", offline, name="offline"),
    path("webpush/save_information", save_info, name="save_webpush_info"),
]
