from os.path import join
from django.http import HttpResponse, JsonResponse
from django.core.files import File
from django_pwa.settings import PWA_SETTINGS


def service_worker(request):
    service_worker_file = File(open(PWA_SETTINGS['worker-location'], 'rb'))
    return HttpResponse(service_worker_file, content_type="text/javascript")


def pwa_manifest(request):
    return JsonResponse(PWA_SETTINGS)
