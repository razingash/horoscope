const CACHE_NAME = 'pwa-cache-v1';
const FILES_TO_CACHE = [
    'en/index.html', // default index.html for PWA (metatags doesn't matter)
    '/favicon.ico',
    '/manifest.webmanifest',
    '/static/json/moon-events/en.json',
    '/static/json/moon-events/ru.json',
    '/static/json/moon-events/pl.json',
];


async function cacheFirst(request) {
    try {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            console.log('Serving from cache:', request.url);
            return cachedResponse;
        }
        console.log('Fetching from network:', request.url);
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            await cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        console.error('CacheFirst error:', error);
        return new Response('Offline', { status: 503, statusText: 'Service Unavailable' });
    }
}

async function networkFirst(request) {
    const cache = await caches.open(CACHE_NAME);

    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            await cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        console.warn('Network request failed, serving from cache:', request.url);
        const cachedResponse = await caches.match(request);
        return cachedResponse || new Response('Offline', { status: 503, statusText: 'Service Unavailable' });
    }
}


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
            }).then((manifest) => {
                const filesToCache = [...FILES_TO_CACHE];

                Object.keys(manifest.files).forEach((filePath) => {
                    if (filePath.endsWith('.css') || filePath.endsWith('.js')) {
                        filesToCache.push(manifest.files[filePath]);
                    }
                });
                const rawDate = new Date();
                const date = rawDate.toISOString().split('T')[0] + "T00:00:00Z";
                const year = rawDate.getFullYear()

                let userLang = (navigator.language || 'en').split('-')[0];
                const supportedLanguages = ['en', 'pl', 'ru'];

                if (!supportedLanguages.includes(userLang)) {
                    userLang = 'en';
                }

                const apiUrls = [
                    `api/horoscope/daily/?language=${userLang}&date=${date}`,
                    `api/horoscope/weekly/?language=${userLang}&date=${date}`,
                    `api/horoscope/monthly/?language=${userLang}&date=${date}`,
                    `api/horoscope/annual/?language=${userLang}&date=${date}`,
                    `api/moon/lunar-forecast/${year}/`,
                    'api/solar-system/map/'
                ];

                const fetchPromises = apiUrls.map((url) => {
                    return fetch(url).then((response) => {
                        if (response.ok) {
                            return cache.put(url, response.clone());
                        }
                    });
                });

                return Promise.all([
                    ...fetchPromises,
                    cache.addAll(filesToCache)
                ]);
            });
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
self.addEventListener('message', (event) => {
    if (event.data.action === 'triggerPush') {
        const messageBody = event.data.body || 'Default notification body';

        // eslint-disable-next-line no-restricted-globals
        self.registration.showNotification('Triggered Push Notification', {
            body: messageBody,
            icon: '/favicon.ico',
        });
    }
});

// eslint-disable-next-line no-restricted-globals
self.addEventListener('fetch', (event) => {
    if (event.request.mode === 'navigate') { // this is necessary to use the same HTML file (metatags aren't important)
        event.respondWith(
            caches.match('en/index.html').then(response => response || fetch(event.request))
        );
        return;
    }

    const url = new URL(event.request.url);
    if (url.pathname.startsWith('/static/json/')) { // Cache First
        event.respondWith(cacheFirst(event.request));
    } else if (url.pathname === '/index.html' || url.pathname.match(/\.(css|js|ico)$/)) { // Cache First
        event.respondWith(cacheFirst(event.request));
    } else if (url.pathname.startsWith('/api/')) {
        event.respondWith(networkFirst(event.request)); // Network first later
    }
});
