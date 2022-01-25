from django.contrib.staticfiles.storage import StaticFilesStorage
from django.contrib.staticfiles.utils import get_files
from django.conf import settings


def find_static_files():
    storage = StaticFilesStorage()
    static_url = getattr(settings, 'STATIC_URL')
    return ['{}{}'.format(static_url, file) for file in get_files(storage)]
