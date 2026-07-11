// 이 사이트는 매일 데이터가 바뀌므로, 콘텐츠를 캐싱하지 않는다.
// (캐싱하면 "어제 데이터가 계속 보이는" 사고가 날 수 있음)
// 서비스 워커는 "설치 가능한 앱"으로 인식되기 위한 최소 요건만 채운다.

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  self.clients.claim();
});

// fetch 이벤트를 그대로 네트워크로 통과시킨다 (캐시 없이 항상 최신 데이터 요청)
self.addEventListener('fetch', (event) => {
  event.respondWith(fetch(event.request));
});
