from django.urls import path
from django_pwa.views import (service_worker, pwa_manifest)

urlpatterns = [
    path('service-worker.js', service_worker),
    path('manifest.json', pwa_manifest)
]
