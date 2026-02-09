# 1. Gömülü Sistemler (Embedded System)

Bu klasör, ESP32-CAM ve motor sürücü (TB6612FNG) entegrasyonu için gerekli tüm gömülü sistem kodlarını ve şemalarını içerir.

## İçerik
- **esp32_firmware:** ESP32 araç kontrol yazılımı.
- **esp32_cam_tb6612_driver:** Kamera ve motor sürücü entegrasyon kodları.
- **arayüz dosyaları:** Araç kontrolü için web arayüzü dosyaları.
- **.vscode:** Bu proje için gerekli VS Code yapılandırma dosyalarını (Arduino ayarları vb.) içerir.

## Devre Bağlantı Şeması (Circuit Diagram)
Aşağıdaki bileşenler ve bağlantılar kullanılmıştır:

*   **ESP32-CAM:** Ana kontrolcü.
*   **TB6612FNG:** Motor sürücü.
*   **MG90 Servo:** Direksiyon kontrolü için.
*   **DC Motorlar:** Sürüş (Drive) ve Direksiyon (Steering) için.
*   **Güç Kaynağı:** 11.1V Batarya.
*   **Voltaj Dönüştürücüler:**
    *   LM2596: 11.1V -> 3.3V (ESP32-CAM beslemesi için).
    *   11.1V -> 5V dönüştürücü (Servo motor için).

### Bağlantı Detayları
- **ESP32-CAM Pinleri:**
    - Motor Sürücü (TB6612FNG) Pinleri: 26 (D), 27 (D)
    - Servo Pin: 12 (veya kodda belirtilen PWM pini)
    - Güç: 3.3V ve GND (LM2596 üzerinden)

**Not:** ESP32-CAM modülü hassas olduğu için voltaj regülasyonuna (LM2596 kullanımı) dikkat ediniz.
