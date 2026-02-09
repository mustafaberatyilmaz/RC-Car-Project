# RC Car Project (ESP32-CAM & SLAM & Flutter)

Bu proje, ESP32-CAM tabanlı, uzaktan kontrol edilebilen ve Visual SLAM (Eşzamanlı Konumlandırma ve Haritalama) teknolojisini kullanan kapsamlı bir RC araç projesidir.

## 🚧 Proje Durumu: Geliştirme Aşamasında (Work in Progress)

Bu proje şu anda aktif olarak geliştirilmektedir. Aşağıdaki alanlarda iyileştirmeler ve güncellemeler devam etmektedir:

*   **SLAM Algoritması:** Düzgün haritalama ve konumlandırma için optimizasyon çalışmaları sürmektedir.
*   **Mekanik Tasarım:** Aracın şasisi ve kamera montajı üzerinde mekanik iyileştirmeler yapılmaktadır.
*   **Yazılım:** Hem gömülü sistem (ESP32) hem de SLAM tarafında, donanım değişikliklerine bağlı olarak yazılım güncellemeleri yapılacaktır.

---

## Proje Bileşenleri

### 1. [Gömülü Sistemler (Embedded System)](./1_Embedded_System/README.TR.md)
Aracın beyni olan ESP32-CAM ve motor sürücü entegrasyonu.
![Devre Şeması](1_Embedded_System/electrical_circuit.png)

### 2. [Mobil Uygulama (Flutter App)](./2_Flutter_App/README.TR.md)
Aracı Wi-Fi üzerinden kontrol etmek ve kamera görüntüsünü izlemek için geliştirilen kullanıcı arayüzü.
![Uygulama Arayüzü](2_Flutter_App/screenshots/drive%20car%20app%20interface.png)

### 3. [SLAM Sistemi (SLAM System)](./3_SLAM_System/README.TR.md)
Aracın ortamı haritalandırmasını sağlayan görsel işlemleme modülü.
![SLAM Haritası](3_SLAM_System/results/2d_map_x-z_slam.png)
