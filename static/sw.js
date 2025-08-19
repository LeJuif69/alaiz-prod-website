const CACHE_NAME = 'alaiz-prod-v1.0.0';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/services',
    '/contact',
    '/label',
    '/artiste',
    '/boutique',
    'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'
];

// Installation du Service Worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Cache ouvert');
                return cache.addAll(urlsToCache);
            })
    );
});

// Activation et nettoyage des anciens caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Suppression du cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Interception des requêtes
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Retourne la réponse mise en cache si elle existe
                if (response) {
                    return response;
                }
                
                // Sinon, effectue la requête réseau
                return fetch(event.request).then(response => {
                    // Vérifie si la réponse est valide
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }
                    
                    // Clone la réponse car elle ne peut être consommée qu'une fois
                    const responseToCache = response.clone();
                    
                    caches.open(CACHE_NAME)
                        .then(cache => {
                            cache.put(event.request, responseToCache);
                        });
                    
                    return response;
                });
            })
            .catch(() => {
                // Retourne une page offline personnalisée si nécessaire
                if (event.request.destination === 'document') {
                    return caches.match('/');
                }
            })
    );
});

// Synchronisation en arrière-plan
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync') {
        console.log('Synchronisation en arrière-plan');
        // Ici vous pourriez synchroniser des données
    }
});

// Notifications push
self.addEventListener('push', event => {
    if (event.data) {
        const options = {
            body: event.data.text(),
            icon: '/static/icons/icon-192x192.png',
            badge: '/static/icons/badge-72x72.png',
            vibrate: [100, 50, 100],
            data: {
                dateOfArrival: Date.now(),
                primaryKey: 1
            },
            actions: [
                {
                    action: 'explore',
                    title: 'Découvrir',
                    icon: '/static/icons/checkmark.png'
                },
                {
                    action: 'close',
                    title: 'Fermer',
                    icon: '/static/icons/xmark.png'
                }
            ]
        };
        
        event.waitUntil(
            self.registration.showNotification('A LAIZ PROD', options)
        );
    }
});

// Gestion des clics sur les notifications
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

console.log('Service Worker A LAIZ PROD initialisé'); 
