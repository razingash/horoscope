/* Network First */

const CACHE_NAME = 'pwa-cache-v1';
const FILES_TO_CACHE = [
    '/index.html',
    '/favicon.ico',
    '/manifest.webmanifest',
    '/static/json/moon-events/en.json',
    '/static/json/moon-events/ru.json',
    '/static/json/moon-events/pl.json',
];


const cacheStaticFiles = (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            return (
                cachedResponse ||
                fetch(event.request).then((networkResponse) => {
                    if (networkResponse && networkResponse.status === 200) {
                        return caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, networkResponse.clone());
                            return networkResponse;
                        });
                    }
                    return networkResponse;
                })
            );
        })
    );
};

const cacheFirst = (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            return (
                cachedResponse ||
                fetch(event.request).then((networkResponse) => {
                    if (networkResponse.ok) {
                        return caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, networkResponse.clone());
                            return networkResponse;
                        });
                    }
                    return networkResponse;
                })
            );
        })
    );
};

const networkFirst = (event) => { // избыточно?
    event.respondWith(
        fetch(event.request)
            .then((networkResponse) => {
                if (networkResponse.ok) {
                    return caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                }
                return networkResponse;
            })
            .catch(() => {
                return caches.match(event.request);
            })
    );
};


// eslint-disable-next-line no-restricted-globals
self.addEventListener('install', (event) => {
    console.log('Service Worker: Installing...');
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Service Worker: Caching Files');
            return cache.addAll(FILES_TO_CACHE);
        })
    );
});


// eslint-disable-next-line no-restricted-globals
self.addEventListener('activate', (event) => {
    console.log('Service Worker: Activated');
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        console.log(`Service Worker: Deleting cache ${cacheName}`);
                        return caches.delete(cacheName);
                    }
                    return undefined;
                })
            );
        })
    );
});


// eslint-disable-next-line no-restricted-globals
self.addEventListener('fetch', (event) => { // перехватчик
    const url = new URL(event.request.url);
    if (url.pathname.startsWith('/static/json/')) { // Cache First
        cacheFirst(event);
    } else if (url.pathname.match(/\.(css|js|ico)$/)) { // Network First
        cacheStaticFiles(event);
    }
});
