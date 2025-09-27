// Service Worker for Chidmano
const CACHE_NAME = 'chidmano-v1';
const urlsToCache = [
    '/',
    '/static/css/modern-ui.css',
    '/static/css/bootstrap.min.css',
    '/static/js/bootstrap.bundle.min.js'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            }
        )
    );
});
