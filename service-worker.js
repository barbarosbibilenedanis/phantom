self.addEventListener('install', function(event) {
    console.log('Service Worker kurulum aşamasında.');
});

self.addEventListener('activate', function(event) {
    console.log('Service Worker aktif.');
});

self.addEventListener('push', function(event) {
    let options = {
        body: event.data ? event.data.text() : 'Varsayılan içerik',
        icon: 'path/to/icon.png',
        badge: 'path/to/badge.png'
    };

    event.waitUntil(
        self.registration.showNotification('Bildirim Başlığı', options)
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(
        clients.openWindow('https://example.com')
    );
});
