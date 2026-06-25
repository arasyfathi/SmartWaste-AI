---
title: SmartWaste AI
emoji: ♻️
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

<div align="center">

# ♻️ SmartWaste AI

**Sistem Deteksi dan Klasifikasi Sampah Real-Time Berbasis Artificial Intelligence**

Dikembangkan sebagai Proyek Akhir Mata Kuliah IMV — Telkom University, Tahun Akademik 2026

---

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![React](https://img.shields.io/badge/React-19-61dafb?logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.8-3178c6?logo=typescript&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange?logo=tensorflow&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8m-Ultralytics-red)
![Cloudinary](https://img.shields.io/badge/Cloudinary-Storage-blue?logo=cloudinary)
![Vercel](https://img.shields.io/badge/Vercel-Frontend-black?logo=vercel)
![HuggingFace](https://img.shields.io/badge/Hugging%20Face-Backend-yellow?logo=huggingface)

</div>

---

## 📑 Daftar Isi

- [📖 Gambaran Umum](#-gambaran-umum)
- [🌍 Latar Belakang](#-latar-belakang)
- [✨ Fitur Utama](#-fitur-utama)
- [🚀 Live Demo](#-live-demo)
- [🏗 Arsitektur Sistem](#-arsitektur-sistem)
- [💻 Tech Stack](#-tech-stack)
- [📁 Struktur Direktori](#-struktur-direktori)
- [🧠 Model Artificial Intelligence](#-model-artificial-intelligence)
- [🗂 Kategori Sampah](#-kategori-sampah)
- [📊 Dataset](#-dataset)
- [📈 Hasil Pelatihan Model](#-hasil-pelatihan-model)
- [⚙️ Instalasi Lokal](#️-instalasi-lokal)
- [🔌 API Endpoints](#-api-endpoints)
- [🚢 Deployment Produksi](#-deployment-produksi)
- [👨‍💻 Tim Pengembang](#-tim-pengembang)
- [📜 Lisensi](#-lisensi)

---

## 📖 Gambaran Umum

**SmartWaste AI** adalah aplikasi web berbasis Kecerdasan Buatan (AI) yang membantu pengguna mengenali dan memilah sampah secara otomatis menggunakan teknologi *Computer Vision* dan *Deep Learning*.

Sistem ini menggabungkan **dua model AI** untuk dua skenario penggunaan yang berbeda:

| Mode | Model AI | Mekanisme |
|------|----------|-----------|
| 📸 **Klasifikasi Gambar** | MobileNetV2 (TensorFlow/Keras) | Pengguna mengunggah foto sampah → model mengklasifikasikan ke 5 kategori + rekomendasi pengelolaan |
| 📷 **Deteksi Real-Time** | YOLOv8m (Ultralytics/PyTorch) | Kamera streaming langsung → deteksi objek sampah dengan *bounding box* dan *confidence score* |

Setiap gambar yang berhasil diklasifikasikan otomatis diunggah ke **Cloudinary** (berjalan di *background thread*, tidak menunda *response* API) dan dicatat di log riwayat prediksi.

---

## 🌍 Latar Belakang

Permasalahan sampah merupakan salah satu tantangan lingkungan terbesar di Indonesia. Kurangnya kesadaran masyarakat dalam memilah sampah berdampak pada:

- Rendahnya efektivitas proses daur ulang
- Meningkatnya volume sampah di Tempat Pembuangan Akhir (TPA)
- Menurunnya efisiensi pengelolaan limbah perkotaan

**SmartWaste AI** dikembangkan sebagai solusi edukatif berbasis AI untuk membantu masyarakat mengenali jenis sampah secara cepat, akurat, dan interaktif — sekaligus memberikan panduan pengelolaan yang tepat per kategori.

---

## ✨ Fitur Utama

- 📸 **Klasifikasi Gambar** — Upload foto sampah, dapatkan prediksi kategori + *confidence score* + rekomendasi pengelolaan
- 📷 **Deteksi Real-Time** — Deteksi objek sampah via webcam dengan *bounding box*, label, dan skor akurasi langsung di *live stream*
- 🔄 **Smoothing Deteksi** — Mekanisme *voting* berbasis `deque` untuk menstabilkan label pada mode kamera dan mengurangi *flickering*
- 💡 **Rekomendasi Pengelolaan** — Tips spesifik per kategori (daur ulang, kompos, pengepul, dll.)
- ☁️ **Penyimpanan Otomatis ke Cloudinary** — Setiap prediksi dibackup secara *asynchronous* tanpa memblokir *response* API
- 🤖 **Deteksi GPU Otomatis** — YOLOv8 menggunakan GPU (CUDA) bila tersedia; *fallback* ke CPU secara otomatis
- ✅ **Validasi File Server-Side** — Tipe dan ukuran file divalidasi di backend (bukan hanya di JavaScript)
- ⚡ **Frontend Modern** — React 19 + TypeScript + Vite: UI responsif, komponen modular, dan performa tinggi

---

## 🚀 Live Demo

> Aplikasi sudah berjalan penuh di lingkungan produksi. Tidak diperlukan instalasi lokal untuk mencoba fitur utama.

| Layanan | URL |
|---------|-----|
| 🌐 **Frontend (Vercel)** | [https://smart-waste-ai-eta.vercel.app](https://smart-waste-ai-eta.vercel.app) |
| ⚙️ **Backend API (Hugging Face)** | [https://fathiarasy-smartwaste.hf.space](https://fathiarasy-smartwaste.hf.space) |
| 📊 **Status Model** | [https://fathiarasy-smartwaste.hf.space/api/status](https://fathiarasy-smartwaste.hf.space/api/status) |

---

## 🏗 Arsitektur Sistem

Proyek ini menggunakan arsitektur **frontend-backend terpisah** (*decoupled architecture*) dengan tiga layanan utama yang saling berkomunikasi:

```
┌─────────────────────────────────────────────────────────────┐
│                    PENGGUNA (Browser)                       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
┌────────────────────────▼────────────────────────────────────┐
│           FRONTEND — Vercel (React + Vite)                  │
│  ┌──────────┐ ┌─────────────┐ ┌──────────┐ ┌───────────┐   │
│  │   Home   │ │ Klasifikasi │ │  Camera  │ │   About   │   │
│  └──────────┘ └──────┬──────┘ └────┬─────┘ └───────────┘   │
└─────────────────────-│─────────────│────────────────────────┘
                        │ POST /api/predict   │ POST /api/camera-frame
                        │ (multipart/form-data) │ (JSON base64)
┌───────────────────────▼─────────────────────▼──────────────┐
│         BACKEND — Hugging Face Spaces (Flask + Gunicorn)    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  app.py — Flask REST API                               │ │
│  │  ├── MobileNetV2 (TensorFlow/Keras) — Klasifikasi      │ │
│  │  ├── YOLOv8m (Ultralytics/PyTorch) — Deteksi RT        │ │
│  │  └── cloudinary_storage.py — Upload async              │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS (Cloudinary SDK)
┌──────────────────────────────▼──────────────────────────────┐
│               STORAGE — Cloudinary                          │
│         (Penyimpanan gambar hasil prediksi)                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Tech Stack

| Layer | Teknologi | Keterangan |
|-------|-----------|------------|
| **Frontend** | React 19, TypeScript 5.8, Vite 6 | UI web modern dengan komponen modular |
| **Routing** | react-router-dom v7 | Navigasi SPA (Single-Page Application) |
| **Backend** | Python 3.11, Flask 3.0, Gunicorn | REST API server produksi |
| **CORS** | flask-cors | Mengizinkan request lintas-*origin* dari Vercel |
| **AI — Klasifikasi** | TensorFlow 2.13+, Keras, MobileNetV2 | Model *image classification* 5 kelas |
| **AI — Deteksi** | Ultralytics YOLOv8m, PyTorch | Model *object detection* real-time |
| **Computer Vision** | OpenCV 4.8+ | Decode, resize, dan konversi frame kamera |
| **Kamera** | WebRTC API (browser-native) | Streaming webcam tanpa plugin |
| **Image Storage** | Cloudinary | Penyimpanan gambar hasil prediksi secara cloud |
| **Deploy Frontend** | Vercel | Hosting static + edge functions |
| **Deploy Backend** | Hugging Face Spaces (Docker SDK) | Container Docker dengan Gunicorn |

---

## 📁 Struktur Direktori

```
smartwaste_ai/
│
├── 📄 Dockerfile                   # Konfigurasi Docker untuk deploy backend ke HF Spaces
├── 📄 requirements.txt             # Python dependencies untuk lingkungan produksi (Docker/HF)
├── 📄 .gitattributes               # Konfigurasi Git LFS (model .keras dan .pt > 100MB)
├── 📄 .gitignore                   # File yang dikecualikan dari version control
├── 📄 DEPLOY_NOTES.md              # Catatan teknis proses deployment
├── 📄 LICENSE
├── 📄 README.md
│
├── 📂 frontend/                    # ◀ UI React — di-deploy ke Vercel
│   ├── index.html                  # Entry HTML (Google Fonts, favicon)
│   ├── package.json                # Dependensi NPM (react, react-router-dom, vite)
│   ├── vite.config.ts              # Konfigurasi Vite (port 3000, proxy)
│   ├── tsconfig.json               # Konfigurasi TypeScript
│   ├── vercel.json                 # Konfigurasi routing SPA untuk Vercel
│   ├── .env.example                # Template variabel lingkungan frontend
│   ├── public/
│   │   └── images/                 # Logo institusi (FTE, laboratorium)
│   └── src/
│       ├── main.tsx                # Entry point ReactDOM + BrowserRouter
│       ├── App.tsx                 # Definisi route seluruh halaman
│       ├── components/
│       │   ├── layout/             # Navbar, Footer, Layout, BackgroundOrnaments
│       │   ├── home/               # StatsBar, FeaturesGrid, HowItWorks, WasteCategories
│       │   └── klasifikasi/        # UploadPanel, ResultsPanel, TipsRow
│       ├── hooks/
│       │   └── useCamera.ts        # Hook WebRTC + real-time detection
│       ├── lib/
│       │   ├── api.ts              # API client (predictImage, sendCameraFrame, getStatus)
│       │   ├── constants.ts        # CLASS_NAMES, COLORS, RECOMMENDATIONS
│       │   └── icons.tsx           # Komponen ikon SVG
│       ├── pages/
│       │   ├── Home.tsx            # Halaman utama
│       │   ├── Klasifikasi.tsx     # Halaman klasifikasi gambar
│       │   ├── Camera.tsx          # Halaman deteksi real-time
│       │   └── About.tsx           # Halaman tentang proyek & tim
│       └── styles/
│           └── globals.css         # Seluruh styling aplikasi (design system)
│
├── 📂 backend/                     # ◀ Flask REST API — di-deploy ke Hugging Face Spaces
│   ├── app.py                      # Inti Flask app: routing, inferensi AI, log prediksi
│   └── cloudinary_storage.py       # Upload gambar ke Cloudinary (background thread)
│
├── 📂 model/                       # ◀ Bobot model AI siap pakai (digunakan oleh backend)
│   ├── classification/
│   │   ├── smartwaste_mobilenetv2.keras   # Model MobileNetV2 — 5 kelas (Git LFS)
│   │   └── class_indices.json             # Pemetaan indeks → nama kelas Keras
│   └── yolo/
│       ├── smartwaste_yolo.pt             # Model YOLOv8m — 5 kelas (Git LFS)
│       ├── data.yaml                      # Konfigurasi dataset YOLO
│       ├── dataset.txt                    # Ringkasan mapping & statistik dataset
│       ├── README.dataset.txt             # Dokumentasi dataset asli (Roboflow)
│       └── README.roboflow.txt            # Info ekspor format Roboflow
│
├── 📂 train/                       # ◀ Skrip pelatihan model (tidak dipakai di produksi)
│   ├── prepare_dataset.py          # Preprocessing & remap dataset Kaggle (12 kelas → 5)
│   ├── train_keras.py              # Training MobileNetV2 (2 tahap: head + fine-tune)
│   ├── train_yolo.py               # Training YOLOv8m (100 epoch, support resume)
│   ├── evaluate_keras.py           # Evaluasi model Keras (classification report)
│   └── cek_model.py                # Verifikasi path dan kelas model
│
├── 📂 reports/                     # ◀ Grafik & laporan hasil pelatihan
│   ├── mobilenet/
│   │   ├── confusion_matrix.png
│   │   └── training_history.png
│   └── yolov8/
│       ├── confusion_matrix_20260619_1412.png
│       ├── confusion_matrix_normalized_20260619_1412.png
│       └── training_history_20260619_1412.png
│
└── 📂 docs/                        # ◀ Aset dokumentasi (screenshot, diagram)
    └── assets/
        ├── space_main.png
        └── ...
```

> **📌 Catatan untuk Penguji:** Folder `frontend/` berisi seluruh kode UI yang berjalan di Vercel. Folder `backend/` berisi Flask API yang berjalan di Hugging Face. Folder `model/` berisi file bobot AI yang dibaca langsung oleh backend saat container Docker dijalankan. Folder `train/` hanya digunakan saat proses pelatihan ulang model dari awal.

---

## 🧠 Model Artificial Intelligence

### MobileNetV2 — Klasifikasi Gambar

| Properti | Detail |
|----------|--------|
| Arsitektur | MobileNetV2 (*Transfer Learning* dari ImageNet) |
| Framework | TensorFlow 2.13+ / Keras |
| Input | 224 × 224 px, 3 channel (RGB) |
| Output | 5 kelas (softmax) |
| File model | `model/classification/smartwaste_mobilenetv2.keras` |
| Strategi Training | 2 tahap: (1) Head training 15 epoch dengan base *frozen*, (2) Fine-tune 40 layer teratas 20 epoch |
| Augmentasi | Rotasi, flip horizontal, zoom, *brightness shift*, shear |

### YOLOv8m — Deteksi Real-Time

| Properti | Detail |
|----------|--------|
| Arsitektur | YOLOv8 Medium (`yolov8m.pt`) |
| Framework | Ultralytics / PyTorch |
| Input | 640 × 640 px |
| Output | 5 kelas + *bounding box* + *confidence score* |
| File model | `model/yolo/smartwaste_yolo.pt` |
| Training | 100 epoch di Google Colab (GPU Tesla T4), *best checkpoint* epoch 77 |
| Batch size | 16 (turunkan ke 8 atau 4 jika VRAM < 6 GB) |

---

## 🗂 Kategori Sampah

Kedua model AI menggunakan **5 kelas yang identik**:

| Kategori | Emoji | Warna UI | Panduan Pengelolaan |
|----------|-------|----------|---------------------|
| **Kaca** | 🪟 | `#8b5cf6` (Ungu) | Pisahkan khusus; bungkus pecahan dengan kertas tebal sebelum dibuang |
| **Kertas** | 📄 | `#f59e0b` (Kuning) | Daur ulang; jika terkena minyak/basah, jadikan kompos |
| **Logam** | ⚙️ | `#22c55e` (Hijau) | Jual ke pengepul atau serahkan ke bank sampah |
| **Organik** | 🌿 | `#84cc16` (Lime) | Jadikan kompos atau pupuk organik |
| **Plastik** | ♻️ | `#06b6d4` (Cyan) | Pisahkan, cuci, dan kirim ke tempat daur ulang |

---

## 📊 Dataset

### Dataset 1 — Klasifikasi Gambar (MobileNetV2)

| Properti | Detail |
|----------|--------|
| Sumber | [Garbage Classification — Mostafa Abla (Kaggle)](https://www.kaggle.com/datasets/mostafaabla/garbage-classification) |
| Jumlah gambar | ~15.870 gambar berlabel |
| Kelas asli | 12 kelas (brown-glass, green-glass, metal, paper, plastic, dll.) |
| Kelas setelah remap | 5 kelas (Kaca, Kertas, Logam, Organik, Plastik) |
| Kelas yang dibuang | `clothes`, `shoes`, `trash` — tidak relevan untuk konteks pengelolaan sampah umum |
| Skrip preprocessing | `train/prepare_dataset.py` |

### Dataset 2 — Deteksi Objek (YOLOv8m)

| Properti | Detail |
|----------|--------|
| Sumber | [Garbage Classification 3 — Roboflow Universe](https://universe.roboflow.com/material-identification/garbage-classification-3/dataset/2) |
| Lisensi | CC BY 4.0 |
| Jumlah gambar | 10.464 gambar |
| Total anotasi | 74.090 *bounding box* |
| Kelas asli | 6 kelas (BIODEGRADABLE, CARDBOARD, GLASS, METAL, PAPER, PLASTIC) |
| Kelas setelah remap | 5 kelas — `CARDBOARD` + `PAPER` digabung menjadi `kertas`; `CLOTH` dibuang |
| Format anotasi | YOLO `.txt` per gambar |
| Preprocessing | Resize 416×416, auto-orientation, augmentasi flip & rotasi |

---

## 📈 Hasil Pelatihan Model

### MobileNetV2 (Klasifikasi Gambar)

| Metrik | Nilai |
|--------|-------|
| Training Accuracy | 90.02% |
| Validation Accuracy | 93.53% |
| Validation Loss | 0.3274 |

> Grafik *training history* dan *confusion matrix* tersedia di `reports/mobilenet/`.

### YOLOv8m (Deteksi Real-Time)

*Best checkpoint* di epoch 77 dari total 100 epoch training.

| Metrik | Nilai |
|--------|-------|
| mAP50 (semua kelas) | 0.654 |
| mAP50-95 | 0.456 |
| Precision | 0.752 |
| Recall | 0.590 |

**mAP50 per kelas:**

| Kelas | Precision | Recall | mAP50 | mAP50-95 |
|-------|-----------|--------|-------|----------|
| Kaca | 0.904 | 0.712 | 0.822 | 0.616 |
| Kertas | 0.739 | 0.548 | 0.635 | 0.486 |
| Logam | 0.851 | 0.643 | 0.728 | 0.504 |
| Organik | 0.815 | 0.496 | 0.629 | 0.357 |
| Plastik | 0.451 | 0.551 | 0.454 | 0.314 |

> Grafik *training history* dan *confusion matrix* tersedia di `reports/yolov8/`.

---

## ⚙️ Instalasi Lokal

> **Catatan:** Untuk sekadar mencoba aplikasi, gunakan [Live Demo](#-live-demo) di atas. Instalasi lokal diperlukan hanya untuk pengembangan atau eksperimen lebih lanjut.

### Prasyarat

- Python 3.11+
- Node.js 18+
- Git + Git LFS (untuk mengunduh file model berukuran besar)

### 1. Clone Repository

```bash
git clone https://github.com/arasyfathi/SmartWaste-AI.git
cd SmartWaste-AI

# Unduh file model via Git LFS
git lfs pull
```

### 2. Setup Backend

```bash
cd backend

# Install dependencies (CPU-only, cocok untuk pengembangan lokal)
pip install -r ../requirements.txt

# Jalankan backend
python app.py
```

Backend akan berjalan di `http://localhost:7860`.

> ⚠️ Pastikan file model ada di `model/classification/` dan `model/yolo/` sebelum menjalankan backend.

### 3. Setup Frontend

Buka terminal baru:

```bash
cd frontend
npm install

# Salin template environment
cp .env.example .env
# Isi VITE_API_URL dengan http://localhost:7860 (atau URL HF Spaces untuk produksi)

npm run dev
```

Frontend akan berjalan di `http://localhost:3000`.

---

## 🔌 API Endpoints

Semua endpoint tersedia di backend (`https://fathiarasy-smartwaste.hf.space`).

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/` | Status backend & info endpoint |
| `POST` | `/api/predict` | Prediksi gambar (multipart/form-data) |
| `POST` | `/api/camera-frame` | Deteksi satu frame kamera (JSON base64) |
| `GET` | `/api/status` | Status model yang dimuat (Keras & YOLO) |
| `GET` | `/api/health` | *Health check* sederhana |
| `GET` | `/api/debug-files` | Debug lokasi file model di server |

### Contoh: `POST /api/predict`

```bash
curl -X POST https://fathiarasy-smartwaste.hf.space/api/predict \
  -F "image=@foto_sampah.jpg"
```

Response:

```json
{
  "success": true,
  "prediction": "Plastik",
  "confidence": 94.7,
  "all_scores": {
    "Kaca": 0.3,
    "Kertas": 3.1,
    "Logam": 0.8,
    "Organik": 1.1,
    "Plastik": 94.7
  },
  "recommendation": {
    "icon": "♻️",
    "color": "#06b6d4",
    "action": "Daur Ulang",
    "tips": ["Pisahkan ke tempat sampah daur ulang plastik.", "..."]
  },
  "model_used": "MobileNetV2"
}
```

---

## 🚢 Deployment Produksi

### Frontend → Vercel

File `frontend/vercel.json` sudah dikonfigurasi untuk routing SPA. Deploy otomatis terpicu setiap `git push` ke branch `main`.

```bash
# Build manual (opsional, Vercel membangun otomatis)
cd frontend
npm run build
```

### Backend → Hugging Face Spaces (Docker)

`Dockerfile` di root proyek mendefinisikan container untuk Hugging Face Spaces. Deploy otomatis terpicu setiap `git push hf main`.

```dockerfile
# Gunicorn digunakan sebagai WSGI server produksi
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "--threads", "4", "backend.app:app"]
```

**Environment Secrets** yang wajib diset di Hugging Face Space Settings:

| Secret Key | Keterangan |
|------------|------------|
| `CLOUDINARY_CLOUD_NAME` | Cloud name akun Cloudinary |
| `CLOUDINARY_API_KEY` | API Key Cloudinary |
| `CLOUDINARY_API_SECRET` | API Secret Cloudinary |

---

## 👨‍💻 Tim Pengembang

**Fakultas Teknik Elektro — Telkom University, Tahun Akademik 2026**

| Nama | NIM | Peran |
|------|-----|-------|
| **Fathi Arasy** | 101022400103 | Backend & Frontend Developer |
| **Adelia Afriliani** | 101052300002 | UI/UX Designer & Frontend Developer |
| **Ghalib Hafuza** | 10012400211 | Computer Vision & Model Development |

---

## 📜 Lisensi

Proyek ini dikembangkan untuk keperluan akademik sebagai bagian dari Proyek Akhir Mata Kuliah IMV di Telkom University.

© 2026 SmartWaste AI Team — Telkom University
