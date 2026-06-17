# ♻️ SmartWaste AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16-orange)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-red)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-purple)

### Sistem Klasifikasi dan Deteksi Sampah Real-Time Berbasis Artificial Intelligence

Dikembangkan oleh Mahasiswa Telkom University

</div>

---

# 📑 Daftar Isi

- [📖 Gambaran Umum](#-gambaran-umum)
- [🌍 Latar Belakang](#-latar-belakang)
- [🚀 Status Proyek](#-status-proyek)
- [✨ Fitur Utama](#-fitur-utama)
- [🧠 Model Artificial Intelligence](#-model-artificial-intelligence)
- [🔍 Perbandingan Model AI](#-perbandingan-model-ai)
- [🗂 Kategori Sampah](#-kategori-sampah)
- [📊 Dataset](#-dataset)
- [🚀 Pengembangan Fitur](#-pengembangan-fitur)
- [🏗 Arsitektur Sistem](#-arsitektur-sistem)
- [💻 Tech Stack](#-tech-stack)
- [📁 Struktur Proyek](#-struktur-proyek)
- [⚙️ Instalasi](#️-instalasi)
- [🚀 Cara Penggunaan](#-cara-penggunaan)
- [📈 Hasil Pelatihan Model](#-hasil-pelatihan-model)
- [🖼 Tampilan Aplikasi](#-tampilan-aplikasi)
- [🔮 Pengembangan Selanjutnya](#-pengembangan-selanjutnya)
- [👨‍💻 Tim Pengembang](#-tim-pengembang)
- [📜 Lisensi](#-lisensi)

---

# 📖 Gambaran Umum

SmartWaste AI merupakan aplikasi berbasis Artificial Intelligence yang dirancang untuk membantu pengguna mengenali dan memilah sampah secara otomatis menggunakan teknologi Computer Vision dan Deep Learning.

Sistem ini menggabungkan dua pendekatan Artificial Intelligence:

### 📸 Klasifikasi Gambar

Menggunakan MobileNetV2 untuk mengidentifikasi jenis sampah dari gambar yang diunggah pengguna.

### 📷 Deteksi Sampah Real-Time

Menggunakan YOLOv8 dan OpenCV untuk mendeteksi objek sampah secara langsung melalui kamera dengan bounding box dan confidence score.

Selain memberikan hasil prediksi, sistem juga menampilkan rekomendasi pengelolaan sampah sesuai kategori yang terdeteksi.

---

# 🌍 Latar Belakang

Permasalahan sampah masih menjadi salah satu tantangan lingkungan terbesar di Indonesia.

Kurangnya kesadaran masyarakat dalam memilah sampah menyebabkan:

* Rendahnya efektivitas proses daur ulang
* Meningkatnya jumlah sampah di Tempat Pembuangan Akhir (TPA)
* Menurunnya efisiensi pengelolaan limbah

SmartWaste AI dikembangkan sebagai solusi edukatif berbasis Artificial Intelligence untuk membantu masyarakat mengenali jenis sampah secara cepat dan akurat.

---

## 📁 Struktur Proyek

```
smartwaste_ai/
├── app.py                  # Flask backend
├── requirements.txt        # Dependencies
├── train_keras.py          # Training MobileNetV2
├── train_yolo.py           # Training YOLOv8
├── prepare_dataset.py      # Preprocessing dataset
│
├── model/
│   ├── smartwaste_model.h5     # Keras model (setelah training)
│   ├── smartwaste_yolo.pt      # YOLOv8 model (setelah training)
│   └── class_indices.json      # Mapping kelas
│
├── templates/
│   ├── base.html           # Layout utama (navbar, footer)
│   ├── index.html          # Home Page
│   ├── klasifikasi.html    # Classification Page
│   ├── camera.html         # Camera Real-Time Page
│   └── about.html          # About Page
│
├── static/
│   ├── css/style.css       # Semua style
│   └── js/
│       ├── main.js         # Navbar & utilities
│       ├── klasifikasi.js  # Upload & predict logic
│       └── camera.js       # WebRTC & YOLO real-time
│
└── datasets/               # Folder dataset (tidak di-commit)
    ├── garbage/            # Dataset Keras (per kelas)
    └── smartwaste/         # Dataset YOLO (images + labels)
```

---

## 🧠 Training Model

### A. Keras / MobileNetV2 (untuk halaman Klasifikasi)

**1. Download Dataset dari Kaggle:**
- [Garbage Classification](https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification)
- [Waste Classification](https://www.kaggle.com/datasets/techsash/waste-classification-data)

**2. Ekstrak dan rename folder:**
```bash
python prepare_dataset.py --src datasets/raw --dst datasets/garbage
```

**3. Train:**
```bash
python train_keras.py
```

Output: `model/smartwaste_model.h5`

---

### B. YOLOv8 (untuk halaman Camera Real-Time)

**1. Download Dataset YOLO format dari Kaggle:**
- [Trash Detection YOLOv8](https://www.kaggle.com/datasets/...)

**2. Buat `datasets/smartwaste/data.yaml`:**
```yaml
path: datasets/smartwaste
train: images/train
val:   images/val
nc: 5
names: ['Kaca', 'Kertas', 'Logam', 'Organik', 'Plastik']
```

**3. Train:**
```bash
python train_yolo.py
```

Output: `model/smartwaste_yolo.pt`

---

## 🔌 API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET  | `/`              | Home Page |
| GET  | `/klasifikasi`   | Classification Page |
| GET  | `/camera`        | Camera Real-Time Page |
| GET  | `/about`         | About Page |
| POST | `/api/predict`   | Prediksi gambar (multipart/form-data) |
| POST | `/api/camera-frame` | Deteksi satu frame (JSON base64) |
| GET  | `/api/status`    | Status model yang dimuat |

### Contoh POST `/api/predict`
```bash
curl -X POST http://localhost:5000/api/predict \
  -F "image=@foto_sampah.jpg"
```

Response:
```json
{
  "success": true,
  "prediction": "Plastik",
  "confidence": 94.7,
  "all_scores": {"Plastik": 94.7, "Kertas": 3.1, ...},
  "recommendation": {
    "icon": "♻️",
    "color": "#06b6d4",
    "action": "Daur Ulang",
    "tips": ["Pisahkan ke tempat sampah..."]
  }
}
```

---

## 🎯 Kategori Sampah

| Kategori | Warna | Penanganan |
|----------|-------|------------|
| 🪟 Kaca    | Ungu  | Pisahkan khusus |
| 📄 Kertas  | Kuning | Daur ulang |
| ⚙️ Logam  | Hijau | Jual ke pengepul |
| 🌿 Organik | Lime  | Kompos |
| ♻️ Plastik | Cyan  | Daur ulang |

---

## 🚢 Deploy ke Vercel

1. Tambah `vercel.json` di root:
```json
{
  "version": 2,
  "builds": [{"src": "app.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "app.py"}]
}
```

2. Push ke GitHub dan connect ke Vercel.

---

### base.html

Template dasar yang digunakan seluruh halaman.

Berisi:

* Navbar
* Footer
* Layout utama

---

### index.html

Halaman Home.

Menampilkan:

* Hero section
* Statistik model
* Fitur aplikasi
* Informasi singkat proyek

---

### klasifikasi.html

Halaman klasifikasi gambar.

Menampilkan:

* Upload gambar
* Preview
* Prediksi AI
* Confidence score
* Rekomendasi pengelolaan

---

### camera.html

Halaman deteksi sampah real-time.

Menampilkan:

* Webcam
* Bounding box
* Confidence score
* Hasil deteksi langsung

---

### about.html

Halaman informasi proyek.

Menampilkan:

* Deskripsi proyek
* Teknologi yang digunakan
* Dataset
* Informasi tim pengembang

---

## 🐍 prepare_dataset.py

Script preprocessing dataset.

Tugas utama:

* Membersihkan dataset
* Menggabungkan kelas
* Resize gambar
* Membagi train/validation/test

---

## 🧠 train_keras.py

Script pelatihan MobileNetV2.

Fungsi:

* Training model klasifikasi
* Transfer Learning
* Fine-Tuning
* Evaluasi model

Output:

```text
smartwaste_model.h5
```

---

## 🎯 train_yolo.py

Script pelatihan YOLOv8.

Fungsi:

* Training object detection
* Validasi model
* Export model

Output:

```text
best.pt
last.pt
```

---

## 📘 README.md

Dokumentasi utama proyek.

Berisi:

* Deskripsi proyek
* Cara instalasi
* Cara penggunaan
* Struktur proyek
* Hasil model
* Dokumentasi teknis

```
```

# ⚙️ Instalasi

```bash
git clone https://github.com/arasyfathi/SmartWaste-AI.git

cd SmartWaste-AI

pip install -r requirements.txt

python app.py
```

Akses aplikasi melalui:

```text
http://localhost:5000
```

---

# 🚀 Cara Penggunaan

## Klasifikasi Gambar

1. Buka halaman Klasifikasi
2. Upload gambar sampah
3. Klik Prediksi
4. Lihat hasil klasifikasi
5. Baca rekomendasi pengelolaan

## Deteksi Real-Time

1. Buka halaman Camera
2. Aktifkan webcam
3. Arahkan kamera ke objek sampah
4. Sistem melakukan deteksi secara real-time
5. Hasil ditampilkan dalam bentuk bounding box dan confidence score

---

# 📈 Hasil Pelatihan Model

## MobileNetV2

| Metric              | Value  |
| ------------------- | ------ |
| Accuracy            | 90.02% |
| Validation Accuracy | 93.53% |
| Test Loss           | 0.3274 |

## YOLOv8

Output training:

* best.pt
* last.pt
* labels.jpg
* results.csv

---

# 🖼 Tampilan Aplikasi

Tambahkan screenshot berikut ke folder assets:

* Home Page
* Classification Page
* Camera Detection
* About Page
* YOLO Detection Result

---

# 🔮 Pengembangan Selanjutnya

* Mobile Application Version
* Smart Bin Integration
* Cloud Deployment
* Waste Volume Estimation
* Multi-Language Support
* User Authentication
* Detection History
* AI Analytics Dashboard

---

# 👨‍💻 Tim Pengembang

### Fathi Arasy

Machine Learning & Backend Developer

### Adelia Afriliani

UI/UX Designer & Frontend Developer

### Ghalib Hafuza

Computer Vision & Model Development

---

Telkom University

Tahun Akademik 2026

---

# 📜 Lisensi

Proyek ini dikembangkan untuk keperluan akademik sebagai bagian dari Proyek IMV di Telkom University.

© 2026 SmartWaste AI Team
