# ♻️ SmartWaste AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16-orange?style=for-the-badge&logo=tensorflow)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-red?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-purple?style=for-the-badge)

### Sistem Klasifikasi dan Deteksi Sampah Real-Time Berbasis Artificial Intelligence

Dikembangkan oleh Mahasiswa Telkom University

</div>

---

# 📑 Daftar Isi

- [📖 Gambaran Umum](#-gambaran-umum)
- [🌍 Latar Belakang](#-latar-belakang)
- [🎯 Tujuan Pengembangan](#-tujuan-pengembangan)
- [✨ Fitur Utama](#-fitur-utama)
- [🧠 Model Artificial Intelligence](#-model-artificial-intelligence)
- [📊 Performa Model](#-performa-model)
- [🗂 Kategori Sampah](#-kategori-sampah)
- [📦 Dataset](#-dataset)
- [🏗 Arsitektur Sistem](#-arsitektur-sistem)
- [🛠 Teknologi yang Digunakan](#-teknologi-yang-digunakan)
- [📁 Struktur Proyek](#-struktur-proyek)
- [⚙ Instalasi](#-instalasi)
- [🚀 Cara Menjalankan](#-cara-menjalankan)
- [🔌 API Endpoint](#-api-endpoint)
- [📈 Hasil Pelatihan Model](#-hasil-pelatihan-model)
- [🖼 Tampilan Aplikasi](#-tampilan-aplikasi)
- [👨‍💻 Tim Pengembang](#-tim-pengembang)
- [📜 Lisensi](#-lisensi)

---

# 📖 Gambaran Umum

SmartWaste AI merupakan aplikasi berbasis Artificial Intelligence yang dirancang untuk membantu pengguna mengenali dan memilah sampah secara otomatis menggunakan teknologi Computer Vision dan Deep Learning.

Sistem ini menggabungkan dua pendekatan utama:

### 📸 Klasifikasi Gambar

Menggunakan MobileNetV2 untuk mengidentifikasi jenis sampah dari gambar yang diunggah pengguna.

### 🎥 Deteksi Sampah Real-Time

Menggunakan YOLOv8 dan OpenCV untuk mendeteksi objek sampah secara langsung melalui kamera dengan bounding box dan confidence score.

Selain memberikan hasil prediksi, sistem juga menampilkan rekomendasi pengelolaan sampah berdasarkan kategori yang terdeteksi.

---

# 🌍 Latar Belakang

Permasalahan sampah masih menjadi salah satu tantangan lingkungan terbesar di Indonesia.

Kurangnya kesadaran masyarakat dalam memilah sampah menyebabkan:

- Rendahnya efektivitas proses daur ulang
- Meningkatnya jumlah sampah di Tempat Pembuangan Akhir (TPA)
- Menurunnya efisiensi pengelolaan limbah
- Bertambahnya pencemaran lingkungan

SmartWaste AI dikembangkan sebagai solusi edukatif berbasis Artificial Intelligence untuk membantu masyarakat mengenali jenis sampah secara cepat dan akurat.

---

# 🎯 Tujuan Pengembangan

Tujuan utama pengembangan SmartWaste AI:

- Membantu proses klasifikasi sampah secara otomatis
- Mendukung edukasi pemilahan sampah
- Mengimplementasikan teknologi Artificial Intelligence dalam bidang lingkungan
- Mengembangkan sistem Computer Vision berbasis web
- Mendukung pengelolaan sampah yang lebih efektif

---

# ✨ Fitur Utama

## 📸 Klasifikasi Gambar

- Upload gambar sampah
- Prediksi menggunakan MobileNetV2
- Confidence score
- Visualisasi hasil prediksi
- Rekomendasi pengelolaan sampah

## 🎥 Deteksi Real-Time

- Webcam real-time
- YOLOv8 Object Detection
- Bounding Box
- Confidence Score
- Multi-object Detection

## ♻️ Rekomendasi Pengelolaan Sampah

- Daur ulang
- Kompos
- Penanganan khusus
- Edukasi pengelolaan limbah

---

# 🧠 Model Artificial Intelligence

## MobileNetV2

Digunakan untuk fitur klasifikasi gambar.

Keunggulan:

- Ringan
- Cepat
- Akurasi tinggi
- Cocok untuk aplikasi web

---

## YOLOv8

Digunakan untuk deteksi objek sampah secara real-time.

Keunggulan:

- Real-time Detection
- Multi-object Detection
- Bounding Box Localization
- High Speed Inference

---

# 📊 Performa Model

## MobileNetV2 (Klasifikasi)

| Metric | Nilai |
|----------|----------|
| Training Accuracy | 90.02% |
| Validation Accuracy | 93.53% |
| Test Loss | 0.3274 |

---

## YOLOv8 (Deteksi Objek)

| Metric | Nilai |
|----------|----------|
| Precision | 58.4% |
| Recall | 45.7% |
| mAP@50 | 51.8% |
| mAP@50-95 | 35.3% |

### Performa per Kelas

| Kelas | Precision | Recall | mAP50 |
|---------|---------|---------|---------|
| Organik | 84.2% | 42.5% | 60.6% |
| Karton | 73.4% | 49.0% | 59.1% |
| Kaca | 86.4% | 68.4% | 79.6% |
| Logam | 72.4% | 58.4% | 66.8% |
| Kertas | 6.2% | 9.1% | 7.3% |
| Plastik | 28.0% | 46.7% | 37.4% |

---

# 🗂 Kategori Sampah

| Kategori | Penanganan |
|-----------|------------|
| 🌿 Organik | Kompos |
| ♻️ Plastik | Daur Ulang |
| 📄 Kertas | Daur Ulang |
| 📦 Karton | Daur Ulang |
| ⚙️ Logam | Dijual ke Pengepul |
| 🪟 Kaca | Penanganan Khusus |

---

# 📦 Dataset

Dataset yang digunakan berasal dari beberapa sumber publik:

## Dataset Klasifikasi

- Garbage Classification Dataset (Kaggle)
- Waste Classification Dataset (Kaggle)

## Dataset Deteksi Objek

- Garbage Classification 3 (Roboflow)
- Dataset hasil anotasi tambahan

---

# 🏗 Arsitektur Sistem

```text
Pengguna
    │
    ▼
Website Flask
    │
 ┌──┴───────────────┐
 │                  │
 ▼                  ▼
MobileNetV2      YOLOv8
(Klasifikasi)    (Deteksi)
 │                  │
 ▼                  ▼
Prediksi       Bounding Box
 │                  │
 └──────┬───────────┘
        ▼
Rekomendasi Pengelolaan Sampah
```

---

# 🛠 Teknologi yang Digunakan

## Backend

- Flask
- Python

## Machine Learning

- TensorFlow
- Keras
- MobileNetV2

## Computer Vision

- OpenCV
- YOLOv8
- Ultralytics

## Frontend

- HTML5
- CSS3
- JavaScript

---

# 📁 Struktur Proyek

```text
SmartWaste-AI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── model/
│   ├── classification/
│   └── yolo/
│
├── static/
│   ├── css/
│   ├── js/
│   └── assets/
│
├── templates/
│   ├── index.html
│   ├── klasifikasi.html
│   ├── camera.html
│   └── about.html
│
├── train/
│   ├── train_keras.py
│   └── train_yolo.py
│
└── datasets/
```

---

# ⚙ Instalasi

Clone repository:

```bash
git clone https://github.com/arasyafathi/smartwaste-AI.git

cd smartwaste-AI
```

Install dependency:

```bash
pip install -r requirements.txt
```

Jalankan aplikasi:

```bash
python app.py
```

Akses melalui browser:

```text
http://localhost:5000
```

---

# 🚀 Cara Menjalankan

## Klasifikasi Gambar

1. Buka halaman Klasifikasi
2. Upload gambar sampah
3. Klik Prediksi
4. Lihat hasil klasifikasi
5. Baca rekomendasi pengelolaan

---

## Deteksi Real-Time

1. Buka halaman Camera
2. Izinkan akses webcam
3. Arahkan kamera ke objek sampah
4. Sistem melakukan deteksi secara otomatis
5. Hasil ditampilkan secara real-time

---

# 🔌 API Endpoint

| Method | Endpoint | Deskripsi |
|----------|----------|----------|
| GET | / | Home |
| GET | /klasifikasi | Halaman Klasifikasi |
| GET | /camera | Halaman Kamera |
| GET | /about | Halaman About |
| POST | /api/predict | Prediksi Gambar |
| POST | /api/camera-frame | Deteksi Frame Kamera |
| GET | /api/status | Status Model |

---

# 📈 Hasil Pelatihan Model

## MobileNetV2

```text
Accuracy            : 90.02%
Validation Accuracy : 93.53%
Test Loss           : 0.3274
```

## YOLOv8

```text
Precision : 58.4%
Recall    : 45.7%
mAP@50    : 51.8%
mAP50-95  : 35.3%
```

Model terbaik:

```text
model/yolo/smartwaste_yolo.pt
```

---

# 🖼 Tampilan Aplikasi

## Home Page

Tambahkan screenshot Home Page.

## Halaman Klasifikasi

Tambahkan screenshot halaman klasifikasi.

## Halaman Camera

Tambahkan screenshot hasil deteksi YOLO.

## Halaman About

Tambahkan screenshot halaman about.

---

# 👨‍💻 Tim Pengembang

### Fathi Arasy
### Adelia Afriliani
### Ghalib Hafuza

---

Telkom University

Tahun Akademik 2026

---

# 📜 Lisensi

Proyek ini dikembangkan untuk keperluan akademik sebagai bagian dari Proyek IMV di Telkom University.

© 2026 SmartWaste AI Team
