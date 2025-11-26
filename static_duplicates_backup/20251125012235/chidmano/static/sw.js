// Service Worker for Chidmano
// Simple service worker to prevent 404 errors

const CACHE_NAME = 'chidmano-v1';
const urlsToCache = [
  '/',
  '/static/css/',
  '/static/js/',
  '/static/images/'
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
        // Return cached version or fetch from network
        return response || fetch(event.request);
      }
    )
  );
});