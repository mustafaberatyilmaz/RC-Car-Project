### 🏎️ Visual SLAM RC Car Project

Bu proje, standart bir RC aracı otonom haritalama yeteneğine sahip bir robota dönüştürmeyi hedefler. **ESP32-CAM** mikrodenetleyicisi ve **Python** tabanlı görüntü işleme algoritmaları kullanılarak, LIDAR gibi pahalı sensörler olmadan ortam haritalandırması (SLAM) yapılmaktadır.

#### 🧠 SLAM Algoritması ve Çalışma Mantığı
Projede **Monocular Visual SLAM** (Tek Kameralı SLAM) tekniği kullanılmaktadır. İşleyiş şu şekildedir:
1.  **Görüntü Akışı:** Araç, Wi-Fi üzerinden sürekli görüntü basar.
2.  **ORB Feature Extraction:** Gelen her karede "belirgin noktalar" (köşeler, kenarlar) tespit edilir.
3.  **Optik Akış (Optical Flow):** Noktaların bir sonraki karedeki yer değişimi hesaplanarak aracın hareketi (Odometry) kestirilir.
4.  **Haritalama:** Aracın tahmini konumu referans alınarak, tespit edilen engeller 2 boyutlu bir düzleme (Occupancy Grid) işlenir.

*(Geliştirme Süreci Devam Ediyor: Şu anda kamera hareketinden kaynaklı görüntü bulanıklığını (motion blur) azaltmak için mekanik stabilizasyon ve AKAZE algoritması üzerinde çalışılmaktadır.)*

#### 📸 Gerçek Zamanlı Haritalama Sonuçları

| Gerçek Ortam (Test Parkuru) | Oluşturulan 2D Rota | Algılanan Engeller (Occupancy Grid) |
| :---: | :---: | :---: |
| <img src="https://raw.githubusercontent.com/mustafaberatyilmaz/RC-Car-Project/master/3_SLAM_System/results/photos_of_real_obstacles.jpeg" width="200"> | <img src="https://raw.githubusercontent.com/mustafaberatyilmaz/RC-Car-Project/master/3_SLAM_System/results/2d_map_x-z_slam.png" width="200"> | <img src="https://raw.githubusercontent.com/mustafaberatyilmaz/RC-Car-Project/master/3_SLAM_System/results/occupancy_grid_slam.png" width="200"> |
| *Aracın gördüğü fiziksel engeller.* | *Kuş bakışı çıkarılan yol haritası.* | *Siyah alanlar: Engel, Beyaz: Boş.* |

---
🔗 **Projenin tamamına göz atın:** [RC-Car-Project](https://github.com/mustafaberatyilmaz/RC-Car-Project)
