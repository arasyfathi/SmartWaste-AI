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
<<<<<<< HEAD

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
=======
smartwaste_ai/
├── app.py                  # Flask backend
├── requirements.txt        # Dependencies
│
├── train/
│   ├── train_keras.py      # Training MobileNetV2
│   ├── train_yolo.py       # Training YOLOv8
│   ├── prepare_dataset.py  # Preprocessing dataset
│   ├── evaluate_keras.py   # Evaluasi model Keras
│   └── cek_model.py        # Cek/verifikasi model
│
├── model/
│   ├── classification/
│   │   ├── smartwaste_mobilenetv2.keras   # Model Keras (5 kelas)
│   │   └── class_indices.json             # Mapping kelas Keras
│   └── yolo/
│       ├── smartwaste_yolo.pt      # Model YOLOv8m (5 kelas, hasil remap)
│       ├── data.yaml                # Konfigurasi dataset hasil remap
│       ├── dataset.txt               # Ringkasan dataset & mapping kelas
│       ├── README.dataset.txt        # Dokumentasi dataset asli (Roboflow)
│       └── README.roboflow.txt       # Info ekspor Roboflow
│
├── reports/
│   ├── mobilenet/           # Confusion matrix & training history MobileNetV2
│   └── yolov8/              # Confusion matrix & training history YOLOv8
│
├── templates/
│   ├── base.html           # Layout utama (navbar, footer)
│   ├── index.html          # Home Page
│   ├── klasifikasi.html    # Classification Page
│   ├── camera.html         # Camera Real-Time Page
│   └── about.html          # About Page
│
└── static/
    ├── css/style.css       # Semua style
    └── js/
        ├── main.js         # Navbar & utilities
        ├── klasifikasi.js  # Upload & predict logic
        └── camera.js       # WebRTC & YOLO real-time
>>>>>>> 56a5ce73 (Refactor project structure and add trained AI models)
```

---

# ⚙ Instalasi

<<<<<<< HEAD
Clone repository:
=======
### A. Keras / MobileNetV2 (untuk halaman Klasifikasi)

**1. Download Dataset dari Kaggle:**
- [Garbage Classification (mostafaabla)](https://www.kaggle.com/datasets/mostafaabla/garbage-classification) — 12 kelas asli, diremap ke 5 kelas (Kaca, Kertas, Logam, Organik, Plastik)

**2. Ekstrak dan rename folder:**
```bash
python train/prepare_dataset.py --src datasets/raw --dst datasets/garbage
```

**3. Train:**
```bash
python train/train_keras.py
```

Output: `model/classification/smartwaste_mobilenetv2.keras`

---

### B. YOLOv8 (untuk halaman Camera Real-Time)

**1. Download Dataset dari Roboflow:**
- [GARBAGE CLASSIFICATION 3](https://universe.roboflow.com/material-identification/garbage-classification-3/dataset/2) — format YOLOv8, 6 kelas asli (BIODEGRADABLE, CARDBOARD, GLASS, METAL, PAPER, PLASTIC)

**2. Remap ke 5 kelas Indonesia:**
Kelas asli diremap (CARDBOARD & PAPER digabung menjadi "kertas", CLOTH dibuang) menghasilkan `data.yaml`:
```yaml
train: dataset_remapped/train/images
val:   dataset_remapped/valid/images
test:  dataset_remapped/test/images
nc: 5
names: ['kaca', 'kertas', 'logam', 'organik', 'plastik']
```
Detail lengkap mapping kelas ada di `model/yolo/dataset.txt`.

**3. Train (arsitektur YOLOv8m, 100 epoch dengan resume di Colab):**
```bash
python train/train_yolo.py
```

Output: `model/yolo/smartwaste_yolo.pt`

**Hasil training:** mAP50 = 0.654, mAP50-95 = 0.456 (lihat tabel metrik lengkap di bagian [Hasil Pelatihan Model](#-hasil-pelatihan-model))

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

## 🚢 Deploy

> ⚠️ **Catatan penting:** Vercel dirancang untuk serverless functions ringan, sementara aplikasi ini menjalankan Flask sebagai server penuh dengan TensorFlow + YOLOv8 + OpenCV (>250MB dependencies) serta endpoint kamera real-time yang membutuhkan koneksi persisten. Konfigurasi ini **tidak kompatibel** dengan limit ukuran & timeout serverless function Vercel.

**Strategi yang direkomendasikan — deploy backend ke Render (atau Railway):**

1. Push project ke GitHub (pastikan `model/yolo/smartwaste_yolo.pt` dan `model/classification/smartwaste_mobilenetv2.keras` ikut di-commit, atau gunakan Git LFS jika ukurannya jadi masalah).
2. Buat Web Service baru di [render.com](https://render.com), hubungkan ke repo GitHub.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app` (tambahkan `gunicorn` ke `requirements.txt`) atau `python app.py` untuk testing.
5. Render akan memberikan URL publik (`https://nama-app.onrender.com`) yang sudah menjalankan seluruh fitur termasuk kamera real-time.

**Jika tetap ingin menyertakan Vercel** (misalnya untuk redirect/landing page statis ke backend di Render), Vercel hanya digunakan untuk bagian frontend statis, bukan untuk menjalankan Flask + model AI.

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
>>>>>>> 56a5ce73 (Refactor project structure and add trained AI models)

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

## YOLOv8m (5 Kelas, Hasil Remap)

<<<<<<< HEAD
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
=======
Training 100 epoch (dengan resume di Google Colab, GPU Tesla T4), checkpoint terbaik di epoch 77.

| Metric              | Value  |
| ------------------- | ------ |
| mAP50 (semua kelas) | 0.654  |
| mAP50-95            | 0.456  |
| Precision           | 0.752  |
| Recall              | 0.590  |

**mAP50 per kelas:**

| Kelas    | Precision | Recall | mAP50 | mAP50-95 |
| -------- | --------- | ------ | ----- | -------- |
| Kaca     | 0.904     | 0.712  | 0.822 | 0.616    |
| Kertas   | 0.739     | 0.548  | 0.635 | 0.486    |
| Logam    | 0.851     | 0.643  | 0.728 | 0.504    |
| Organik  | 0.815     | 0.496  | 0.629 | 0.357    |
| Plastik  | 0.451     | 0.551  | 0.454 | 0.314    |

> **Catatan:** Kelas **Plastik** memiliki performa terendah, kemungkinan akibat jumlah instance yang jauh lebih sedikit dibanding kelas lain dalam dataset (class imbalance). Kelas **Organik** juga cukup sering tertukar dengan background pada confusion matrix, kemungkinan karena dominasi jumlah instance organik di dataset. Lihat `reports/yolov8/` untuk grafik training history dan confusion matrix lengkap.

Output training: `best.pt`, `last.pt`, `confusion_matrix.png`, `training_history.png`, `results.csv`
>>>>>>> 56a5ce73 (Refactor project structure and add trained AI models)

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

<<<<<<< HEAD
### Fathi Arasy
### Adelia Afriliani
### Ghalib Hafuza
=======
### Fathi Arasy — NIM 101022400103

Machine Learning & Backend Developer

### Adelia Afriliani — NIM 101052300002

UI/UX Designer & Frontend Developer

### Ghalib Hafuza — NIM 10012400211
>>>>>>> 56a5ce73 (Refactor project structure and add trained AI models)

---

Telkom University

Tahun Akademik 2026

---

# 📜 Lisensi

Proyek ini dikembangkan untuk keperluan akademik sebagai bagian dari Proyek IMV di Telkom University.

© 2026 SmartWaste AI Team
