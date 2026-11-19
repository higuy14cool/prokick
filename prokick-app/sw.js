// ProKick offline cache. Bump CACHE when index.html changes.
const CACHE = 'prokick-v64';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './vendor/three.min.js',
  './audio/crowd-cheer.mp3',
  './icons/icon-192.png',
  './icons/icon-256.png',
  './icons/favicon-32.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './icons/apple-touch-icon.png',
  './icons/apple-touch-icon-152.png',
  './icons/apple-touch-icon-167.png',
  './icons/icon-1024.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET' || new URL(request.url).origin !== self.location.origin) return;

  // Navigations: never show a hosting/proxy error page in place of the game.
  // A cached copy wins over any failed or non-OK response, so the app still
  // opens when the host is unreachable or answers 404/5xx.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request, { cache: 'no-store' })
        .then(response => {
          if (!response.ok) return caches.match('./index.html').then(hit => hit || response);
          const copy = response.clone();
          caches.open(CACHE).then(cache => cache.put('./index.html', copy)).catch(() => {});
          return response;
        })
        .catch(() => caches.match('./index.html').then(hit => hit || Response.error()))
    );
    return;
  }

  event.respondWith(
    caches.match(request).then(hit => hit || fetch(request).then(response => {
      const copy = response.clone();
      caches.open(CACHE).then(cache => cache.put(request, copy)).catch(() => {});
      return response;
    }))
  );
});
