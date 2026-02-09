# 3. SLAM Sistemi (SLAM System)

Bu klasör, Visual SLAM (Eşzamanlı Konumlandırma ve Haritalama) uygulamasının kodlarını ve sonuçlarını içerir.

## İçerik
- **src:** SLAM algoritması Python kodları.
- **results:** SLAM haritalama sonuçları ve gerçek ortam fotoğrafları.

## Yöntem (Method)
Bu projede, ESP32-CAM'den alınan görüntü verileri kullanılarak Python tabanlı bir Görsel SLAM algoritması uygulanmıştır.

### Sonuçlar

#### 2D Harita (X-Z)
![2D Harita](results/2d_map_x-z_slam.png)

#### Doluluk Izgarası (Occupancy Grid)
![Doluluk Izgarası](results/occupancy_grid_slam.png)

#### Gerçek Ortam ve Engeller
![Gerçek Ortam](results/photos_of_real_obstacles.jpeg)
