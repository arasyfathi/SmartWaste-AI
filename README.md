# ♻️ SmartWaste AI

<div align="center">

### Smart Waste Classification & Real-Time Detection System

Sistem klasifikasi dan deteksi sampah berbasis Artificial Intelligence menggunakan MobileNetV2, YOLOv8, Flask, dan OpenCV.

Dikembangkan oleh Mahasiswa Telkom University.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-red)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-purple)

</div>

---

# 📑 Daftar Isi

* [📖 Gambaran Umum](#-gambaran-umum)
* [🌍 Latar Belakang](#-latar-belakang)
* [🚀 Fitur Utama](#-fitur-utama)
* [🧠 Model Artificial Intelligence](#-model-artificial-intelligence)
* [🗂 Kategori Sampah](#-kategori-sampah)
* [📊 Dataset](#-dataset)
* [🏗 Arsitektur Sistem](#-arsitektur-sistem)
* [💻 Tech Stack](#-tech-stack)
* [🎨 UI/UX Design](#-uiux-design)
* [📂 Struktur Proyek](#-struktur-proyek)
* [⚙️ Instalasi](#️-instalasi)
* [🚀 Cara Penggunaan](#-cara-penggunaan)
* [📈 Hasil Model](#-hasil-model)
* [🖼 Tampilan Aplikasi](#-tampilan-aplikasi)
* [🔮 Pengembangan Selanjutnya](#-pengembangan-selanjutnya)
* [👥 Tim Pengembang](#-tim-pengembang)
* [📜 Lisensi](#-lisensi)

---

# 📖 Gambaran Umum

SmartWaste AI merupakan aplikasi berbasis Artificial Intelligence yang dirancang untuk membantu pengguna mengenali dan memilah sampah secara otomatis menggunakan teknologi Computer Vision dan Deep Learning.

Aplikasi ini mengintegrasikan:

* MobileNetV2 untuk klasifikasi gambar
* YOLOv8 untuk deteksi objek real-time
* Flask sebagai backend web framework
* OpenCV untuk pemrosesan kamera
* HTML, CSS, dan JavaScript untuk frontend

Pengguna dapat melakukan klasifikasi sampah melalui gambar maupun kamera secara real-time dan memperoleh rekomendasi pengelolaan sampah berdasarkan kategori yang terdeteksi.

---

# 🌍 Latar Belakang

Permasalahan sampah masih menjadi salah satu tantangan lingkungan terbesar di Indonesia.

Kurangnya kesadaran masyarakat dalam memilah sampah menyebabkan:

* Rendahnya efektivitas proses daur ulang
* Meningkatnya jumlah sampah di TPA
* Menurunnya efisiensi pengelolaan limbah

SmartWaste AI dikembangkan sebagai solusi edukatif berbasis Artificial Intelligence yang membantu masyarakat mengenali jenis sampah secara cepat dan mudah.

---

# 🚀 Fitur Utama

## 📸 Klasifikasi Gambar

* Upload gambar sampah
* Prediksi kategori sampah
* Confidence score
* Probabilitas tiap kategori
* Rekomendasi pengelolaan sampah

## 📷 Deteksi Sampah Real-Time

* Webcam integration
* Real-time object detection
* Bounding box visualization
* Multi-object detection
* Confidence score
* OpenCV camera processing

## 🌐 Website Features

* Responsive Design
* Modern Dashboard
* Interactive UI
* Waste Information
* About Project Page

---

# 🧠 Model Artificial Intelligence

## MobileNetV2

Model klasifikasi gambar berbasis Transfer Learning.

### Konfigurasi

| Parameter    | Nilai                |
| ------------ | -------------------- |
| Arsitektur   | MobileNetV2          |
| Framework    | TensorFlow / Keras   |
| Input Size   | 224 × 224            |
| Jumlah Kelas | 5                    |
| Tugas        | Image Classification |

### Kategori

* Plastik
* Kertas
* Kaca
* Logam
* Organik

### Performa

| Metric    | Nilai  |
| --------- | ------ |
| Accuracy  | 90.02% |
| Precision | 88%    |
| Recall    | 90%    |
| F1 Score  | 89%    |

---

## YOLOv8

Model deteksi objek untuk kamera real-time.

### Kategori

* Organik
* Karton
* Kaca
* Logam
* Kertas
* Plastik

### Kemampuan

* Real-Time Detection
* Multi-Object Detection
* Bounding Box Detection
* Camera Integration

---

# 🗂 Kategori Sampah

### MobileNetV2 (5 Kelas)

| Kategori |
| -------- |
| Plastik  |
| Kertas   |
| Kaca     |
| Logam    |
| Organik  |

### YOLOv8 (6 Kelas)

| Kategori |
| -------- |
| Organik  |
| Karton   |
| Kaca     |
| Logam    |
| Kertas   |
| Plastik  |

---

# 📊 Dataset

## MobileNetV2 Dataset

Sumber:

https://www.kaggle.com/datasets/mostafaabla/garbage-classification

Kategori:

* Plastik
* Kertas
* Kaca
* Logam
* Organik

---

## YOLOv8 Dataset

Sumber:

https://universe.roboflow.com/material-identification/garbage-classification-3/dataset/2

Kategori:

* Organik
* Karton
* Kaca
* Logam
* Kertas
* Plastik

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

### Backend

* Python
* Flask

### Frontend

* HTML5
* CSS3
* JavaScript

### Tools

* VS Code
* Git
* GitHub
* Figma

---

# 🎨 UI/UX Design

Figma Mockup:

https://www.figma.com/design/OzYxRog70sqp7um7R8FMlk/SmartWaste-AI-%E2%80%94-Mock-up-NEW

Konsep desain menggunakan tema:

* Sustainability
* Smart Environment
* Green Technology
* Eco-Friendly Interface

Dengan fokus pada pengalaman pengguna yang sederhana, modern, dan mudah digunakan.

---

# 📂 Struktur Proyek

```text
SmartWaste-AI
│
├── app.py
├── requirements.txt
│
├── model/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── klasifikasi.html
│   ├── camera.html
│   ├── about.html
│   └── base.html
│
├── train_keras.py
├── train_yolo.py
│
└── README.md
```

---

# ⚙️ Instalasi

Clone repository:

```bash
git clone https://github.com/arasyfathi/SmartWaste-AI.git

cd SmartWaste-AI
```

Install dependency:

```bash
pip install -r requirements.txt
```

Jalankan aplikasi:

```bash
python app.py
```

Akses:

```text
http://localhost:5000
```

---

# 🚀 Cara Penggunaan

## Klasifikasi Gambar

1. Buka halaman Klasifikasi.
2. Upload gambar sampah.
3. Klik tombol Prediksi.
4. Lihat hasil klasifikasi.
5. Baca rekomendasi pengelolaan.

## Deteksi Real-Time

1. Buka halaman Camera.
2. Aktifkan webcam.
3. Arahkan kamera ke objek sampah.
4. Sistem melakukan deteksi secara real-time.
5. Hasil tampil dalam bentuk bounding box dan confidence score.

---

# 📈 Hasil Model

## MobileNetV2

| Metric              | Hasil  |
| ------------------- | ------ |
| Accuracy            | 90.02% |
| Validation Accuracy | 93.53% |
| Test Loss           | 0.3274 |

## YOLOv8

Output Training:

* best.pt
* last.pt
* confusion_matrix.png
* results.csv
* labels.jpg

---

# 🖼 Tampilan Aplikasi

Tambahkan screenshot berikut:

* Home Page
* Classification Page
* Real-Time Detection Page
* About Page

Contoh:

```md
![Home](static/images/home-preview.png)
```
# 👥 Tim Pengembang

### Fathi Arasy

### Adelia Afriliani

### Ghalib Hafuza
---

Telkom University

2026

---

# 📜 Lisensi

Proyek ini dikembangkan untuk keperluan akademik sebagai bagian dari Project IMV Telkom University.

© 2026 SmartWaste AI Team
