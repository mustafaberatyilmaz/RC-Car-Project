# 1. Gömülü Sistemler (Embedded System)

Bu klasör, projenin donanım kalbini oluşturur. ESP32-CAM modülü ile TB6612FNG motor sürücüsünün entegrasyonu burada gerçekleştirilmiştir.

## 🛠 Donanım Mimarisi

### ESP32-CAM Neden Seçildi?
Bu projede ESP32-CAM'in seçilme nedeni, hem Wi-Fi hem de Bluetooth özelliklerine sahip olması ve dahili bir kamera modülü (OV2640) barındırmasıdır. Arduino Uno veya Nano gibi kartlara kıyasla çok daha yüksek işlem gücüne (Dual-core 240MHz) sahiptir, bu da görüntü aktarımı için kritiktir.

### TB6612FNG Motor Sürücü
Klasik L298N sürücülere göre çok daha verimlidir. MOSFET tabanlı yapısı sayesinde voltaj düşümü (voltage drop) çok daha azdır, bu da pilden alınan enerjinin daha büyük kısmının motorlara gitmesini sağlar. Ayrıca çok daha az ısınır.

### Güç Dağıtımı (Power Distribution)
ESP32-CAM, güç dalgalanmalarına karşı çok hassastır. Yetersiz akım veya voltaj düşmesi durumunda "Brownout Detect" hatası verip kapanır. Bu yüzden:
*   **LM2596 (3.3V):** Doğrudan ESP32'yi beslemek için ayarlanabilir voltaj regülatörü kullanılmıştır. 
*   **Ayrı Hatlar:** Servo motorlar ani akım çektiğinde voltajı düşürebilir, bu yüzden servo beslemesi ve mikrodenetleyici beslemesi paralel hatlardan sağlanmıştır.

## 🔌 Bağlantı Şeması (Circuit)

![Devre Şeması](electrical_circuit.png)

### Pin Konfigürasyonu
*   **GPIO 12:** Servo motor PWM kontrolü için kullanılır. (Not: SD kart kullanılırsa bu pin çakışabilir, dikkat edilmelidir).
*   **GPIO 26 & 27:** TB6612FNG'nin AIN1 ve AIN2 girişlerine bağlanarak DC motorun yönünü kontrol eder.
*   **GPIO 4:** Dahili Flaş LED (Gerekirse aydınlatma için kullanılabilir).

## Yazılım Yapısı
Kod, bir Web Server oluşturur. `/stream` url'sinden sürekli MJPEG yayını yaparken, `/action?go=forward` gibi URL parametreleri ile motor komutlarını dinler. Bu "Asenkron Web Sunucusu" yapısı, aynı anda hem görüntü yollayıp hem komut alabilmeyi sağlar.
