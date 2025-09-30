// Service Worker for Chidmano
const CACHE_NAME = 'chidmano-v2';
const STATIC_ASSETS = [
    '/static/css/modern-ui.css',
    '/static/css/bootstrap.min.css',
    '/static/js/bootstrap.bundle.min.js'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(STATIC_ASSETS);
            })
    );
});

self.addEventListener('fetch', function(event) {
    const req = event.request;
    const url = new URL(req.url);

    // cache-first for static assets
    if (url.pathname.startsWith('/static/')) {
        event.respondWith(
            caches.match(req).then(function(cached) {
                return (
                    cached || fetch(req).then(function(res) {
                        const resClone = res.clone();
                        caches.open(CACHE_NAME).then(function(cache) {
                            cache.put(req, resClone);
                        });
                        return res;
                    })
                );
            })
        );
        return;
    }

    // network-first for HTML/API
    event.respondWith(
        fetch(req)
            .then(function(res) {
                return res;
            })
            .catch(function() {
                return caches.match(req);
            })
    );
});
