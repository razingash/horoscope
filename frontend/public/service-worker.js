const CACHE_NAME = 'pwa-cache-v1';
const FILES_TO_CACHE = [
    'en/index.html', // default index.html for PWA (metatags doesn't matter)
    '/favicon.ico',
    '/manifest.webmanifest',
    '/static/json/moon-events/en.json',
    '/static/json/moon-events/ru.json',
    '/static/json/moon-events/pl.json',
];


const cacheFirst = (event) => {
    console.log("работает Cache First")
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                console.log('Serving from cache:', event.request.url);
                return cachedResponse;
            }

            console.log('Fetching from network:', event.request.url);
            return fetch(event.request).then((networkResponse) => {
                if (networkResponse.ok) {
                    return caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                }
                return networkResponse;
            });
        })
    );
};

const networkFirst = (event) => {
    event.respondWith(
        fetch(event.request)
            .then((networkResponse) => {
                if (networkResponse.ok) { // networkResponse && networkResponse.status === 200
                    return caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                }
                return caches.match(event.request);
            })
            .catch(() => {
                return caches.match(event.request);
            })
    );
};


// eslint-disable-next-line no-restricted-globals
self.addEventListener('install', (event) => {
    console.log('Service Worker: Installing...');
    // eslint-disable-next-line no-restricted-globals
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Service Worker: Caching Files');
            return fetch('asset-manifest.json').then((response) => {
                return response.json();
            }).then((manifest) => { // улучшить
                const filesToCache = [...FILES_TO_CACHE];

                Object.keys(manifest.files).forEach((filePath) => {
                    if (filePath.endsWith('.css') || filePath.endsWith('.js')) {
                        filesToCache.push(manifest.files[filePath]);
                    }
                });

                return cache.addAll(filesToCache);
            });
        })
    );
});


// eslint-disable-next-line no-restricted-globals
self.addEventListener('activate', (event) => {
    console.log('Service Worker: Activated');
    // eslint-disable-next-line no-restricted-globals
    self.clients.claim();
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
    if (event.request.mode === 'navigate') { // this is necessary to use the same HTML file (metatags aren't important)
        event.respondWith(
            caches.match('en/index.html').then(response => response || fetch(event.request))
        );
        return;
    }

    const url = new URL(event.request.url);
    if (url.pathname.startsWith('/static/json/')) { // Cache First
        cacheFirst(event);
    } else if (url.pathname === '/index.html' || url.pathname.match(/\.(css|js|ico)$/)) { // Network First
        cacheFirst(event);
    }
});
