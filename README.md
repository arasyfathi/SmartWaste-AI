# ♻️ SmartWaste AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16-orange)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-red)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-purple)

### Smart Waste Classification & Real-Time Detection System using Artificial Intelligence

Developed by Telkom University Students

</div>

---

# 📖 Overview

SmartWaste AI adalah aplikasi berbasis Artificial Intelligence yang dirancang untuk membantu pengguna mengenali dan memilah sampah secara otomatis menggunakan teknologi Computer Vision dan Deep Learning.

Sistem menyediakan dua metode identifikasi:

### 🖼 Image Classification

Pengguna mengunggah gambar sampah dan sistem akan mengklasifikasikan jenis sampah menggunakan model MobileNetV2.

### 📷 Real-Time Waste Detection

Pengguna dapat menggunakan kamera secara langsung untuk mendeteksi objek sampah secara real-time menggunakan model YOLOv8 dan OpenCV.

Selain memberikan hasil prediksi, sistem juga menampilkan confidence score dan rekomendasi pengelolaan sampah yang sesuai.

---

# 🌍 Background

Salah satu permasalahan utama dalam pengelolaan sampah adalah rendahnya kesadaran masyarakat dalam melakukan pemilahan sampah berdasarkan jenisnya.

Kesalahan dalam pemilahan menyebabkan:

* Sulitnya proses daur ulang
* Meningkatnya jumlah sampah di TPA
* Menurunnya efisiensi pengolahan limbah

Melalui SmartWaste AI, pengguna dapat dengan mudah mengenali jenis sampah hanya melalui gambar atau kamera sehingga proses pemilahan dapat dilakukan dengan lebih cepat dan akurat.

---

# ✨ Main Features

## 📸 Image Classification

* Upload gambar sampah
* Preview gambar sebelum diproses
* Prediksi kategori sampah
* Confidence score
* Per-class probability
* Waste management recommendation

---

## 📷 Real-Time Camera Detection

* Webcam integration
* Real-time object detection
* Bounding box visualization
* Multi-object detection
* Confidence score display
* YOLOv8 inference
* OpenCV camera processing

---

## 🌐 Website Features

* Responsive Design
* Dark Theme Interface
* Modern Dashboard
* AI Performance Statistics
* About Project Page
* Dataset Information
* Technology Overview

---

# 🧠 Artificial Intelligence Models

## MobileNetV2 Classification Model

Model klasifikasi gambar menggunakan Transfer Learning dari MobileNetV2.

### Configuration

| Parameter       | Value                         |
| --------------- | ----------------------------- |
| Architecture    | MobileNetV2                   |
| Framework       | TensorFlow / Keras            |
| Input Size      | 224 × 224                     |
| Classes         | 5                             |
| Training Method | Transfer Learning             |
| Dataset         | Kaggle Garbage Classification |

### Performance

| Metric    | Score  |
| --------- | ------ |
| Accuracy  | 90.02% |
| Precision | 88%    |
| Recall    | 90%    |
| F1 Score  | 89%    |

---

## YOLOv8 Detection Model

Model deteksi objek untuk fitur kamera real-time.

### Configuration

| Parameter    | Value                           |
| ------------ | ------------------------------- |
| Architecture | YOLOv8                          |
| Framework    | Ultralytics                     |
| Task         | Object Detection                |
| Dataset      | Roboflow Garbage Classification |
| Input Source | Webcam                          |
| Output       | Bounding Box + Confidence       |

---

# 🗂 Waste Categories

SmartWaste AI mampu mengenali lima kategori sampah berikut:

| Icon | Category | Description                    |
| ---- | -------- | ------------------------------ |
| ♻️   | Plastic  | Botol plastik, kemasan plastik |
| 📄   | Paper    | Kertas dan kardus              |
| 🔮   | Glass    | Kaca hijau, coklat, dan bening |
| ⚙️   | Metal    | Kaleng dan logam               |
| 🌿   | Organic  | Sampah organik dan biologis    |

---

# 📊 Dataset

## Dataset Klasifikasi

### Garbage Classification Dataset

Source:

https://www.kaggle.com/datasets/mostafaabla/garbage-classification

### Original Classes

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

### Merged Categories

| Final Category | Original Classes                        |
| -------------- | --------------------------------------- |
| Plastic        | plastic                                 |
| Paper          | paper + cardboard                       |
| Glass          | green-glass + brown-glass + white-glass |
| Metal          | metal                                   |
| Organic        | biological                              |

---

## Dataset Deteksi

### Garbage Classification Dataset v2

Source:

https://universe.roboflow.com/material-identification/garbage-classification-3/dataset/2

Dataset ini digunakan untuk melatih model YOLOv8 agar mampu melakukan deteksi objek sampah secara real-time.

---

# 🏗 System Architecture

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

## Artificial Intelligence

* TensorFlow
* Keras
* MobileNetV2
* YOLOv8
* OpenCV
* NumPy
* Pillow

---

## Backend

* Flask
* Python

---

## Frontend

* HTML5
* CSS3
* JavaScript

---

## Deployment

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
│           ├── weights
│           │   ├── best.pt
│           │   └── last.pt
│           │
│           ├── labels.jpg
│           ├── results.csv
│           ├── train_batch0.jpg
│           ├── train_batch1.jpg
│           └── train_batch2.jpg
│
├── static
│   ├── css
│   │   └── style.css
│   │
│   ├── images
│   │   ├── logo-tf.png
│   │   └── logo-lab.png
│   │
│   ├── js
│   │   ├── main.js
│   │   ├── klasifikasi.js
│   │   └── camera.js
│   │
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

---

# ⚙️ Installation

Clone repository

```bash
git clone https://github.com/yourusername/SmartWaste-AI.git
```

Masuk ke folder project

```bash
cd SmartWaste-AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Jalankan aplikasi

```bash
python app.py
```

Buka browser

```bash
http://localhost:5000
```

---

# 🚀 Usage

## Classification

1. Buka halaman Klasifikasi
2. Upload gambar sampah
3. Klik tombol Prediksi
4. Lihat hasil klasifikasi
5. Baca rekomendasi pengelolaan

---

## Camera Detection

1. Buka halaman Camera
2. Aktifkan webcam
3. Arahkan kamera ke objek sampah
4. Sistem mendeteksi objek secara real-time
5. Hasil ditampilkan dalam bentuk bounding box dan confidence score

---

# 📈 Training Results

## MobileNetV2

### Training Configuration

* Image Size : 224×224
* Batch Size : 32
* Optimizer : Adam
* Transfer Learning
* Fine Tuning

### Result

| Metric              | Value  |
| ------------------- | ------ |
| Accuracy            | 90.02% |
| Validation Accuracy | 93.53% |
| Test Loss           | 0.3274 |

---

## YOLOv8

### Training Configuration

* Framework : Ultralytics YOLOv8
* Dataset : Roboflow Garbage Dataset
* Task : Object Detection

### Outputs

* best.pt
* last.pt
* labels.jpg
* results.csv
* training batches

---

# 🖼 Screenshots

## Home Page

Tambahkan screenshot Home Page di sini.

```markdown
![Home](assets/homepage.png)
```

---

## Classification Page

```markdown
![Classification](assets/classification.png)
```

---

## Camera Detection

```markdown
![Camera](assets/camera-detection.png)
```

---

## About Page

```markdown
![About](assets/about.png)
```

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

# 📌 Project Enhancement

SmartWaste AI tidak hanya memenuhi seluruh kebutuhan proyek yang diberikan, tetapi juga menambahkan fitur lanjutan berupa:

### Original Requirement

✅ Upload gambar

✅ Prediksi jenis sampah

✅ Confidence score

✅ Rekomendasi pengelolaan

---

### Additional Features

✅ Real-Time Camera Detection

✅ YOLOv8 Object Detection

✅ OpenCV Integration

✅ Multi-object Detection

✅ Bounding Box Visualization

Dengan tambahan ini, SmartWaste AI mampu melakukan identifikasi sampah baik dari gambar statis maupun video real-time.

---

# 🔮 Future Improvements

* Mobile Application Version
* Cloud Deployment
* Smart Bin Integration
* Waste Volume Estimation
* Multi-Language Support
* User Authentication
* Detection History
* AI Analytics Dashboard

---

# 👨‍💻 Team

### SmartWaste AI Team

**Fathi Arasy**

WEB

---

**Adelia Afriliani**

UI/UX

---

**Ghalib Hafuza**

MODEL

---

Telkom University

Academic Year 2026

---

# 📜 License

This project was developed for educational purposes as part of the Artificial Intelligence Project at Telkom University.

© 2026 SmartWaste AI Team
