# RC Car Project (ESP32-CAM & SLAM & Flutter)

Bu proje, görüntü işleme ve uzaktan kontrol yeteneklerini birleştiren gelişmiş bir RC araç platformudur. Projenin temel amacı, düşük maliyetli donanımlar (ESP32-CAM) kullanarak otonom sürüş ve haritalama (SLAM) yeteneklerinin sınırlarını zorlamaktır.

## 📸 Araç Görünümü
*(Lütfen aracın fotoğrafını `rc_car.jpg` adıyla bu klasöre kaydedin)*
![RC Araç](rc_car.jpeg)

---

## 🚧 Proje Durumu: Geliştirme Aşamasında (Work in Progress)

Bu proje aktif bir Ar-Ge projesidir. Şu anki odak noktaları:
*   **SLAM Optimizasyonu:** ORB ve AKAZE gibi öznitelik çıkarıcıların performans karşılaştırmaları yapılmaktadır.
*   **Mekanik Stabilizasyon:** Kamera titreşimini azaltmak için şasi üzerinde sönümleme çalışmaları sürmektedir.
*   **Gecikme Düşürme:** Görüntü aktarımındaki gecikmeyi (latency) minimize etmek için UDP ve WebSocket alternatifleri test edilmektedir.

---

## Teknik Detaylar ve Bileşenler

### 1. [Gömülü Sistemler (Embedded System)](./1_Embedded_System/README.TR.md)
Aracın donanım katmanıdır.
*   **ESP32-CAM:** Hem ana işlemci hem de kamera modülü olarak görev yapar. Görüntüyü yakalar ve Wi-Fi üzerinden yayınlar.
*   **TB6612FNG:** L298N'e göre çok daha verimli ve ısınmayan bir motor sürücüdür. PWM sinyalleri ile hassas hız kontrolü sağlar.
*   **Güç Yönetimi:** LM2596 regülatörleri ile sisteme kararlı 3.3V ve 5V sağlanır, bu da ESP32'nin "Brownout" hatalarını önler.

### 2. [Mobil Uygulama (Flutter App)](./2_Flutter_App/README.TR.md)
Aracın kontrol merkezidir.
*   **Teknoloji:** Google Flutter (Dart) ile geliştirilmiştir, bu sayede hem Android hem iOS'ta yüksek performansla çalışır.
*   **İletişim:** HTTP stream üzerinden görüntüyü alır ve REST API benzeri isteklerle motor komutlarını gönderir.
*   **Arayüz:** Kullanıcı dostu bir joystick ve gerçek zamanlı video akışı sunar.

### 3. [SLAM Sistemi (SLAM System)](./3_SLAM_System/README.TR.md)
Aracın "gözü" ve "beyni"dir.
*   **Visual SLAM:** Sadece tek bir kamera (Monocular) kullanarak ortamın 3 boyutlu haritasını çıkarır.
*   **Python & OpenCV:** Görüntü işleme algoritmaları bilgisayar tarafında (PC) çalışarak ESP32'nin işlem yükünü hafifletir.
*   **Özellik Çıkarımı:** Görüntüdeki belirgin noktaları (köşeler, kenarlar) tespit ederek aracın hareketini hesaplar.
