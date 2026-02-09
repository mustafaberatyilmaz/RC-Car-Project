# Gerçek Zamanlı Monoküler SLAM Projesi - İş Planı
## Platform: Windows 10/11 | GPU: RTX 4050 | Hedef: Bu Gece Tamamlanacak

## 📋 PROJE ÖZETİ

**Seçilen Yaklaşım:** **Python-based pySLAM + AI Entegrasyonu**  
**Neden Bu Seçim:**
- ✅ Windows'da kolay kurulum
- ✅ Python ile hızlı geliştirme
- ✅ CUDA/GPU desteği
- ✅ Gerçek zamanlı görselleştirme
- ✅ AI modül entegrasyonu için hazır altyapı
- ✅ Bu gece bitirebileceğiniz kapsamda

---

## ⏰ ZAMAN PLANI

1. **Ortam Kurulumu**: Anaconda, Libraries
2. **pySLAM Kurulumu**: (Python scriptleri ile değiştirildi)
3. **Webcam Entegrasyonu**: Test ve Kalibrasyon
4. **AI Modülü**: YOLOv8 ile nesne tespiti
5. **Harita Görselleştirme**: 3D Trajectory
6. **Test ve Optimizasyon**

---

## 🔧 KURULUM VE KULLANIM

### 1. Ortam Hazırlığı
```bash
pip install -r requirements.txt
```

### 2. Kamera Kalibrasyonu
```bash
python calibrate_camera.py
```
*Not: Satranç tahtası desenini göstererek en az 15 görüntü kaydedin ('c' tuşu).*

### 3. Testler
- Webcam testi için: `python test_webcam.py`
- Temel SLAM testi için: `python slam_webcam.py`

### 4. AI Destekli SLAM (Ana Uygulama)
```bash
python slam_ai.py
```
- Bu script, YOLOv8 ile dinamik nesneleri (insan, araba vb.) filtreleyerek daha stabil bir haritalama yapar.
- Çıkmak için 'q' tuşuna basın.

### 5. Harita Görselleştirme
```bash
python visualize_map.py
```
- Oluşturulan `trajectory.npy` dosyasını 3D olarak çizer.

---

## 📂 DOSYA YAPISI

- `requirements.txt`: Gerekli kütüphaneler
- `config/webcam_config.yaml`: Kamera ve SLAM ayarları
- `calibrate_camera.py`: Kamera kalibrasyon scripti
- `test_webcam.py`: Basit kamera testi
- `slam_webcam.py`: Temel özellik tabanlı SLAM
- `slam_ai.py`: YOLO entegreli gelişmiş SLAM
- `visualize_map.py`: Harita görselleştirici

---
## PERFORMANS İPUÇLARI
- RTX 4050 GPU ile 30+ FPS almanız beklenir.
- Hız için `yolov8n.pt` (nano) modeli kullanılmaktadır.