# 2. Flutter Mobil Uygulama (Flutter App)

Bu uygulama, aracın uzaktan kumandası olarak görev yapar. Modern mobil geliştirme standartlarına uygun olarak Flutter framework'ü ile geliştirilmiştir.

## 📱 Uygulama Mimarisi

### Arayüz Tasarımı
Uygulama, **Landscape (Yatay)** modda çalışacak şekilde tasarlanmıştır. Bu sayede ekranın sol tarafı direksiyon kontrolü, sağ tarafı ise gaz/fren kontrolü için optimize edilmiştir. Arkaplanda ise kesintisiz kamera görüntüsü oynatılır.

### Video Akışı (Video Streaming)
ESP32-CAM'den gelen görüntü **MJPEG (Motion JPEG)** formatındadır. Flutter tarafında bu akış, kare kare (frame-by-frame) işlenerek ekrana çizdirilir. Bu yöntem, RTSP gibi protokolere göre daha düşük gecikme (latency) sunar, ancak bant genişliği kullanımı daha yüksektir.

### Ağ İletişimi (Networking)
Uygulama ile araç arasındaki iletişim HTTP protokolü üzerinden sağlanır:
1.  **Görüntü Alma:** `http://<IP_ADDRESS>:81/stream` adresine sürekli bir GET isteği yapılır.
2.  **Kontrol Komutları:** Kullanıcı joystick'i hareket ettirdiğinde, arka planda `http://<IP_ADDRESS>/action?go=left` gibi hafif HTTP istekleri gönderilir. Bu istekler "fire-and-forget" mantığıyla çalışır, yani cevap beklenmez, böylece arayüz donmaz.

## Arayüz
![Uygulama Arayüzü](screenshots/drive%20car%20app%20interface.png)

### Demo Videosu
[Demo Videosunu İzle](drive%20car%20video.mp4)

## Gelecek Güncellemeler
*   **WebSocket:** Kontrol komutlarının HTTP yerine WebSocket üzerinden gönderilmesi planlanmaktadır. Bu sayede TCP el sıkışma (handshake) süreleri ortadan kaldırılarak tepki süresi daha da iyileştirilecektir.
