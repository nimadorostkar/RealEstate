var timestamp = new Date().getTime();

var cacheName = `django-pwa-${timestamp}`;
var filesToCache = [
    '/',
    '/static/icons/icon-32x32.png',
    '/static/icons/icon-128x128.png',
    '/static/icons/icon-144x144.png',
    '/static/icons/icon-152x152.png',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-256x256.png',
    '/static/icons/icon-512x512.png',
];

async function install() {
    const cache = await caches.open(cacheName);
    await cache.addAll(filesToCache);
}

async function deleteCaches() {
    const keys = await caches.keys();
    return Promise.all(
        keys.map(function (key) {
            if (cacheName.indexOf(key) === -1) {
                return caches.delete(key);
            }
        }));
}

async function loadFromCache(url) {
    return await caches.match(url);
}

async function loadFromNetwork(url) {
    const cache = await caches.open(cacheName);
    try {
        const response = await fetch(url);
        const responseClone = response.clone();
        await cache.put(url, responseClone);
        return response
    } catch (e) {
        return await cache.match(url);
    }
}

async function respond(event) {
    const url = event.request.clone();
    return await loadFromCache(url) || await loadFromNetwork(url)
}

self.addEventListener('install', install);

self.addEventListener('activate', (event) => {
    event.waitUntil(
        deleteCaches()
    )
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        respond(event)
    );
});