# 3. SLAM Sistemi (SLAM System)

Bu modül, projenin en karmaşık ve deneysel kısmıdır. Visual SLAM (Görsel Eşzamanlı Konumlandırma ve Haritalama) algoritmalarını içerir.

## 🧠 Algoritma Nasıl Çalışır?

Bu sistem **Monocular SLAM** (Tek Kameralı SLAM) prensibine dayanır. Süreç şu adımlardan oluşur:

1.  **Görüntü Alımı:** ESP32-CAM'den gelen video akışı Python/OpenCV tarafından okunur.
2.  **Öznitelik Çıkarımı (Feature Extraction):** Her karede belirgin noktalar (köşeler, doku değişimleri) tespit edilir. Bu proje kapsamında **ORB (Oriented FAST and Rotated BRIEF)** algoritması, hızı ve verimliliği nedeniyle tercih edilmiştir.
3.  **Eşleştirme (Matching):** Bir önceki karede bulunan noktalar ile yeni karedeki noktalar eşleştirilir. Bu, kameranın (yani aracın) ne kadar ve ne yöne hareket ettiğini anlamamızı sağlar.
4.  **Poz Kestirimi (Pose Estimation):** Noktaların hareketinden yola çıkarak "Odometry" hesaplanır. Bu, aracın uzaydaki (X, Y, Z) konumunu verir.
5.  **Haritalama (Mapping):** Hesaplanan konumlar ve görülen noktalar birleştirilerek ortamın 2 boyutlu (2D) veya 3 boyutlu (3D) bir haritası oluşturulur.

### Kullanılan Teknolojiler
*   **Python:** Ana programlama dili.
*   **OpenCV:** Görüntü işleme kütüphanesi.
*   **NumPy:** Matris hesaplamaları için.

## 📊 Sonuçlar ve Analiz

Aşağıdaki tabloda algoritmanın gerçek ortamdaki çıktısı, oluşturulan 2D harita ve doluluk ızgarası yan yana karşılaştırılmıştır.

| Gerçek Ortam ve Engeller | 2D Harita (X-Z) | Doluluk Izgarası |
| :---: | :---: | :---: |
| <img src="results/photos_of_real_obstacles.jpeg" width="100%"> | <img src="results/2d_map_x-z_slam.png" width="100%"> | <img src="results/occupancy_grid_slam.png" width="100%"> |
| *Testin yapıldığı fiziksel ortam.* | *Kuş bakışı araç rotası.* | *Algılanan engeller (Beyaz: Boş, Siyah: Dolu).* |

## Zorluklar ve Gelecek Çalışmalar
Tek kamera ile derinlik algılamak (Depth Perception) zordur. Bu nedenle haritanın ölçeği (scale) belirsiz olabilir (yani haritada 1 birim, gerçekte 10cm mi 1m mi olduğu tam bilinemeyebilir). İleride **Stereo Kamera** veya **IMU (İvmeölçer)** sensör füzyonu ile bu sorunun çözülmesi hedeflenmektedir.
