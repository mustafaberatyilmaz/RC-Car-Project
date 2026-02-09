# RC Car Project (ESP32-CAM & SLAM & Flutter)

Bu proje, görüntü işleme, gömülü sistemler ve mobil uygulama geliştirme disiplinlerini bir araya getiren kapsamlı bir otonom/yarı-otonom araç platformudur. Projenin temel amacı, düşük maliyetli donanımlar (ESP32-CAM) kullanarak, genellikle LIDAR gibi pahalı sensörlerle yapılan SLAM (Eşzamanlı Konumlandırma ve Haritalama) işleminin sadece bir kamera ile (Visual SLAM) gerçekleştirilebilirliğini araştırmaktır.

---

## 🚧 Proje Durumu: Aktif Geliştirme (Active Development)

Bu proje bir hobi projesinin ötesinde, gerçek zamanlı veri işleme ve kablosuz iletişim üzerine bir Ar-Ge çalışmasıdır.

### Mevcut Geliştirmeler
*   **SLAM Algoritma Karşılaştırması:** Görsel odometri için **ORB (Oriented FAST and Rotated BRIEF)** ve **AKAZE** algoritmalarının performansları (FPS vs Doğruluk) kıyaslanmaktadır. ESP32'nin sınırlı bant genişliği nedeniyle görüntünün sıkıştırılma oranı ile öznitelik kaybı arasındaki denge optimize edilmektedir.
*   **Mekanik İyileştirmeler:** Araç hareket halindeyken oluşan titreşimler (Rolling Shutter etkisi), SLAM algoritmasının "poz kaybı" (pose loss) yaşamasına neden olmaktadır. Bunu engellemek için kamera modülü için sünger destekli bir sönümleme sistemi tasarlanmaktadır.
*   **İletişim Protokolü:** TCP/IP tabanlı HTTP akışı güvenilirdir ancak "Handshake" süreleri nedeniyle gecikme yaratabilir. Daha düşük gecikme için **UDP** tabanlı görüntü aktarımı üzerinde çalışılmaktadır.

---

## 🛠 Teknik Mimari ve Detaylar

### 1. [Gömülü Sistemler (Embedded System)](./1_Embedded_System/README.TR.md) - Donanım Katmanı
Aracın sinir sistemi ESP32-CAM modülüdür.
*   **Çift Çekirdek (Dual Core) Kullanımı:** ESP32'nin çift çekirdekli yapısı verimli kullanılmıştır. `APP_CPU` (Core 1) ana döngüyü ve Wi-Fi iletişimini yönetirken, `PRO_CPU` (Core 0) kamera sensöründen veri okuma işlemlerini üstlenir.
*   **Motor Sürücü Mantığı:** TB6612FNG, PWM (Darbe Genişlik Modülasyonu) sinyalleri ile motorların hızını analog gibi kontrol etmemizi sağlar. L298N'den farklı olarak MOSFET çıkışlı olduğu için enerji verimliliği %95 seviyelerindedir.
*   **Güç Regülasyonu:** 3 adet 18650 pil (seri bağlı, ~12V) kullanılır. LM2596 "Buck Converter" ile voltaj, ısıya dönüşmeden verimli bir şekilde 5V ve 3.3V'a düşürülür.

### 2. [Mobil Uygulama (Flutter App)](./2_Flutter_App/README.TR.md) - Kontrol Katmanı
Kullanıcı deneyimi odaklı kontrol arayüzü.
*   **Durum Yönetimi (State Management):** Uygulama içinde anlık veri akışı (hız, bağlantı durumu) **Provider** paketi ile yönetilir. Bu sayede gereksiz "Widget Rebuild" işlemleri engellenerek yüksek FPS elde edilir.
*   **Asenkron İletişim:** Görüntü akışı ve kontrol komutları tamamen asenkron (Future/Stream) yapıda çalışır. Video paketleri işlenirken arayüz (UI) thread'i bloklanmaz.

### 3. [SLAM Sistemi (SLAM System)](./3_SLAM_System/README.TR.md) - Algılama Katmanı
Aracın dünyayı algılama biçimi.
*   **Monocular Visual SLAM:** Tek bir kamera ile derinlik kestirimi (Depth Estimation) yapmak zordur. Bu projede, ardışık görüntü kareleri arasındaki "Piksel Hareketi" (Optical Flow) ve bilinen kamera parametreleri (Intrinsic Matrix) kullanılarak "Epipolar Geometri" hesaplamaları yapılır.
*   **Loop Closure:** Araç daha önce geçtiği bir yeri tanıdığında (Bag of Words tekniği ile), haritada biriken kayma (Drift) hatasını geriye dönük olarak düzeltir.

---

## 📸 Araç Görünümü

<img src="rc_car.jpeg" width="400" alt="RC Araç Fotoğrafı">
