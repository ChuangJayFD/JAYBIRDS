importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey:            "AIzaSyDam2mLWL2T2y1dx1fLXQdGA0KnKdi6jEU",
  authDomain:        "jaybirds-37083.firebaseapp.com",
  projectId:         "jaybirds-37083",
  storageBucket:     "jaybirds-37083.appspot.com",
  messagingSenderId: "1006771346653",
  appId:             "1:1006771346653:web:1d49c7041413b51e190f34"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  const { title, body, icon, url } = payload.data || payload.notification || {};
  self.registration.showNotification(title || 'JAYBIRDS VOTE', {
    body:  body  || 'JAYへの今日の投票は済みましたか？',
    icon:  icon  || '/remindicon.png',
    badge: '/remindicon.png',
    data:  { url: url || 'https://vote.produce101.jp/' },
    actions: [
      { action: 'vote', title: '今すぐ投票 🗳️' },
      { action: 'close', title: 'あとで' }
    ]
  });
});

self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  if (event.action === 'close') return;
  const url = (event.notification.data && event.notification.data.url)
    || 'https://vote.produce101.jp/';
  event.waitUntil(clients.openWindow(url));
});


