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
```

---

## 🧠 Training Model

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

## YOLOv8m (5 Kelas, Hasil Remap)

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

### Fathi Arasy — NIM 101022400103

Machine Learning & Backend Developer

### Adelia Afriliani — NIM 101052300002

UI/UX Designer & Frontend Developer

### Ghalib Hafuza — NIM 10012400211

Computer Vision & Model Development

---

Telkom University

Tahun Akademik 2026

---

# 📜 Lisensi

Proyek ini dikembangkan untuk keperluan akademik sebagai bagian dari Proyek IMV di Telkom University.

© 2026 SmartWaste AI Team
