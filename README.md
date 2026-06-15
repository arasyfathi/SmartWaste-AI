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

# 🚀 Status Proyek

| Modul                       | Status                |
| --------------------------- | --------------------- |
| MobileNetV2 Classification  | ✅ Selesai             |
| YOLOv8 Real-Time Detection  | ✅ Selesai             |
| Flask Web Integration       | ✅ Selesai             |
| Waste Recommendation System | ✅ Selesai             |
| Responsive Web Interface    | ✅ Selesai             |
| Deployment Cloud            | 🚧 Dalam Pengembangan |

---

# ✨ Fitur Utama

## 📸 Klasifikasi Gambar

* Upload gambar sampah
* Preview gambar
* Prediksi kategori sampah
* Confidence score
* Probabilitas tiap kategori
* Rekomendasi pengelolaan sampah

### 📷 Deteksi Sampah Real-Time

* Integrasi webcam
* Real-time object detection
* Bounding box visualization
* Multi-object detection
* Confidence score display
* YOLOv8 inference
* OpenCV camera processing

### 🌐 Website Features

* Responsive Design
* Modern Dashboard
* Statistik Model AI
* Informasi Dataset
* Informasi Teknologi
* Halaman Tentang Proyek

---

# 🧠 Model Artificial Intelligence

## MobileNetV2

Model klasifikasi gambar berbasis Transfer Learning.

### Konfigurasi

| Parameter    | Nilai                           |
| ------------ | ------------------------------- |
| Arsitektur   | MobileNetV2                     |
| Framework    | TensorFlow / Keras              |
| Ukuran Input | 224 × 224                       |
| Jumlah Kelas | 5                               |
| Tugas        | Image Classification            |
| Dataset      | Garbage Classification (Kaggle) |

### Performa

| Metrik    | Nilai  |
| --------- | ------ |
| Accuracy  | 90.02% |
| Precision | 88%    |
| Recall    | 90%    |
| F1 Score  | 89%    |

---

## YOLOv8

Model deteksi objek untuk fitur kamera real-time.

### Konfigurasi

| Parameter    | Nilai                     |
| ------------ | ------------------------- |
| Arsitektur   | YOLOv8                    |
| Framework    | Ultralytics               |
| Jumlah Kelas | 6                         |
| Tugas        | Object Detection          |
| Input        | Webcam                    |
| Output       | Bounding Box + Confidence |

---

# 🔍 Perbandingan Model AI

| Spesifikasi            | MobileNetV2        | YOLOv8        |
| ---------------------- | ------------------ | ------------- |
| Tugas                  | Klasifikasi Gambar | Deteksi Objek |
| Input                  | Upload Gambar      | Kamera        |
| Jumlah Kelas           | 5                  | 6             |
| Real-Time              | ❌                  | ✅             |
| Bounding Box           | ❌                  | ✅             |
| Multi Object Detection | ❌                  | ✅             |
| Confidence Score       | ✅                  | ✅             |

---

# 🗂 Kategori Sampah

SmartWaste AI menggunakan dua model AI dengan konfigurasi kategori yang berbeda.

## MobileNetV2 (5 Kategori)

* ♻️ Plastik
* 📄 Kertas
* 🔮 Kaca
* ⚙️ Logam
* 🌿 Organik

## YOLOv8 (6 Kategori)

* 🌿 Organik
* 📦 Karton
* 🔮 Kaca
* ⚙️ Logam
* 📄 Kertas
* ♻️ Plastik

Model YOLOv8 menambahkan kategori **Karton** secara terpisah sehingga mampu melakukan identifikasi yang lebih spesifik dibandingkan model klasifikasi.

---

# 📊 Dataset

## Dataset Klasifikasi

**Garbage Classification Dataset**

Sumber:

https://www.kaggle.com/datasets/mostafaabla/garbage-classification

Kategori akhir MobileNetV2:

* Plastik
* Kertas
* Kaca
* Logam
* Organik

Pada dataset ini, kategori **cardboard** digabungkan ke dalam kategori **paper**.

---

## Dataset Deteksi

**Garbage Classification Dataset v2**

Sumber:

https://universe.roboflow.com/material-identification/garbage-classification-3/dataset/2

Kategori YOLOv8:

* Organik
* Karton
* Kaca
* Logam
* Kertas
* Plastik

---

# 🚀 Pengembangan Fitur

Pada implementasi awal, SmartWaste AI hanya menggunakan MobileNetV2 untuk klasifikasi gambar dengan 5 kategori sampah.

Sebagai pengembangan lanjutan, ditambahkan fitur:

* YOLOv8 Object Detection
* Real-Time Camera Detection
* OpenCV Integration
* Multi-Object Detection
* Bounding Box Visualization
* Cardboard Detection

Dengan pengembangan ini, sistem mampu melakukan identifikasi sampah secara langsung melalui kamera secara real-time.

---

# 🏗 Arsitektur Sistem

```text
User
 │
 ▼
SmartWaste AI Website
 │
 ├── Upload Image
 │      │
 │      ▼
 │   MobileNetV2
 │      │
 │      ▼
 │ Classification Result
 │
 └── Camera Detection
        │
        ▼
      OpenCV
        │
        ▼
      YOLOv8
        │
        ▼
 Detection Result
        │
        ▼
 Recommendation
```

---

# 💻 Tech Stack

### Artificial Intelligence

* TensorFlow
* Keras
* MobileNetV2
* YOLOv8
* OpenCV
* NumPy
* Pillow

### Backend

* Flask
* Python

### Frontend

* HTML5
* CSS3
* JavaScript

### Deployment

* GitHub
* Vercel

---

# 📁 Project Structure

```text
SMARTWASTE_AI
│
├── app.py
├── requirements.txt
│
├── datasets
│   ├── garbage
│   ├── raw
│   └── yolo
│
├── model
│   ├── smartwaste_model.h5
│   ├── smartwaste_yolo.pt
│   └── class_indices.json
│
├── logs
│   ├── stage1
│   └── stage2
│
├── runs
│   └── detect
│       └── smartwaste
│           └── weights
│
├── static
│   ├── css
│   ├── images
│   ├── js
│   └── uploads
│
├── templates
│   ├── base.html
│   ├── index.html
│   ├── klasifikasi.html
│   ├── camera.html
│   └── about.html
│
├── prepare_dataset.py
├── train_keras.py
├── train_yolo.py
└── README.md
```

## 📄 File & Folder Description

### app.py

File utama aplikasi Flask yang bertugas menjalankan web server, mengatur routing halaman, menerima request dari frontend, dan menghubungkan website dengan model AI.

**Fungsi:**

* Menjalankan Flask Server
* Routing halaman website
* Memanggil model klasifikasi
* Menjalankan fitur kamera real-time
* Mengirim hasil prediksi ke frontend

---

### requirements.txt

Berisi seluruh library Python yang dibutuhkan oleh proyek.

**Contoh dependency:**

* Flask
* TensorFlow
* OpenCV
* Ultralytics
* NumPy
* Pillow

Digunakan saat instalasi:

```bash
pip install -r requirements.txt
```

---

## 📂 datasets/

Folder yang berisi seluruh dataset yang digunakan selama proses pengembangan dan pelatihan model.

### datasets/raw/

Dataset asli hasil download dari Kaggle sebelum dilakukan preprocessing.

**Isi dataset:**

* battery
* biological
* cardboard
* clothes
* green-glass
* brown-glass
* white-glass
* metal
* paper
* plastic
* shoes
* trash

---

### datasets/garbage/

Dataset hasil preprocessing dan penggabungan kelas menjadi 5 kategori utama:

* Plastik
* Kertas
* Kaca
* Logam
* Organik

Dataset ini digunakan untuk melatih MobileNetV2.

---

### datasets/yolo/

Dataset Object Detection yang berasal dari Roboflow.

Digunakan untuk melatih model YOLOv8.

Struktur:

```text
yolo/
├── train
├── valid
├── test
└── data.yaml
```

---

## 📂 model/

Folder yang menyimpan model AI yang telah dilatih.

### smartwaste_model.h5

Model klasifikasi berbasis MobileNetV2.

Digunakan untuk:

* Upload gambar
* Prediksi jenis sampah
* Confidence score

---

### smartwaste_yolo.pt

Model YOLOv8 yang digunakan untuk fitur deteksi real-time.

Digunakan untuk:

* Bounding box detection
* Real-time camera inference
* Multi-object detection

---

### class_indices.json

Mapping indeks output model ke nama kelas.

Contoh:

```json
{
  "0": "glass",
  "1": "metal",
  "2": "organic",
  "3": "paper",
  "4": "plastic"
}
```

---

## 📂 logs/

Folder penyimpanan log proses training MobileNetV2.

### stage1/

Menyimpan hasil training awal (head training).

### stage2/

Menyimpan hasil fine-tuning model.

Digunakan untuk:

* Monitoring loss
* Monitoring accuracy
* Evaluasi training

---

## 📂 runs/

Folder otomatis yang dihasilkan oleh YOLOv8 selama proses training.

### runs/detect/smartwaste/

Berisi seluruh artefak training object detection.

---

### weights/

Model hasil training YOLO.

#### best.pt

Model terbaik berdasarkan performa validasi.

Digunakan saat deployment.

#### last.pt

Checkpoint model pada epoch terakhir.

Digunakan untuk melanjutkan training.

---

### labels.jpg

Visualisasi distribusi label dataset.

---

### results.csv

Menyimpan hasil training YOLO setiap epoch.

Berisi:

* Precision
* Recall
* mAP50
* mAP50-95
* Loss

---

### train_batch0.jpg – train_batchN.jpg

Contoh batch training yang digunakan YOLO selama proses pelatihan.

---

## 📂 static/

Folder aset statis website.

---

### static/css/

Berisi file styling website.

#### style.css

Mengatur:

* Warna tema
* Layout
* Responsivitas
* Animasi
* Dark mode

---

### static/js/

Berisi seluruh logika frontend.

#### main.js

Fungsi umum website.

#### klasifikasi.js

Mengatur:

* Upload gambar
* Preview gambar
* Request prediksi
* Menampilkan hasil klasifikasi

#### camera.js

Mengatur:

* Akses webcam
* Real-time detection
* Menampilkan bounding box

---

### static/images/

Menyimpan:

* Logo proyek
* Ikon
* Asset visual

---

### static/uploads/

Folder sementara untuk menyimpan gambar yang diunggah pengguna.

---

## 📂 templates/

Folder template HTML yang dirender oleh Flask.

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

Proyek ini dikembangkan untuk keperluan akademik sebagai bagian dari mata kuliah Artificial Intelligence di Telkom University.

© 2026 SmartWaste AI Team
