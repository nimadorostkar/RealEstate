from os.path import join
from django.conf import settings

PWA_SETTINGS = dict()

PWA_SETTINGS['name'] = getattr(settings, 'PWA_NAME', 'test app')
PWA_SETTINGS['short_name'] = getattr(settings, 'PWA_SHORT_NAME', 'test_app')
PWA_SETTINGS['start_url'] = getattr(settings, 'PWA_START_URL', '.')
PWA_SETTINGS['display'] = getattr(settings, 'PWA_DISPLAY', 'standalone')
PWA_SETTINGS['background_color'] = getattr(settings, 'PWA_BACKGROUND_COLOR', '#fff')
PWA_SETTINGS['description'] = getattr(settings, 'PWA_DESCRIPTION', 'this is a simple test')
PWA_SETTINGS['theme_color'] = getattr(settings, 'PWA_THEME_COLOR', '#fff')
pwa_icons = [
    {
        "src": "/static/icons/icon-128x128.png",
        "sizes": "128x128",
        "type": "image/png"
    }, {
        "src": "/static/icons/icon-144x144.png",
        "sizes": "144x144",
        "type": "image/png"
    }, {
        "src": "/static/icons/icon-152x152.png",
        "sizes": "152x152",
        "type": "image/png"
    }, {
        "src": "/static/icons/icon-192x192.png",
        "sizes": "192x192",
        "type": "image/png"
    }, {
        "src": "/static/icons/icon-256x256.png",
        "sizes": "256x256",
        "type": "image/png"
    }, {
        "src": "/static/icons/icon-512x512.png",
        "sizes": "512x512",
        "type": "image/png"
    }
]
PWA_SETTINGS['icons'] = getattr(settings, 'PWA_ICONS', pwa_icons)
default_worker_location = join(settings.STATIC_ROOT, 'django_pwa', 'service-worker.js')
PWA_SETTINGS['worker-location'] = getattr(settings, 'PWA_WORKER_LOCATION', default_worker_location)
