# ♻️ SmartWaste AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![React](https://img.shields.io/badge/React-19-61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-5.8-3178c6)
![Vite](https://img.shields.io/badge/Vite-6-purple)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13%2B-orange)
![YOLOv8](https://img.shields.io/badge/YOLOv8m-Ultralytics-red)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-purple)

### Sistem Klasifikasi dan Deteksi Sampah Real-Time Berbasis Artificial Intelligence

Dikembangkan oleh Mahasiswa Telkom University — Tahun Akademik 2026

</div>

---

# 📑 Daftar Isi

- [📖 Gambaran Umum](#-gambaran-umum)
- [🌍 Latar Belakang](#-latar-belakang)
- [✨ Fitur Utama](#-fitur-utama)
- [🧠 Model Artificial Intelligence](#-model-artificial-intelligence)
- [🗂 Kategori Sampah](#-kategori-sampah)
- [📊 Dataset](#-dataset)
- [🏗 Arsitektur Sistem](#-arsitektur-sistem)
- [💻 Tech Stack](#-tech-stack)
- [📁 Struktur Proyek](#-struktur-proyek)
- [⚙️ Instalasi](#️-instalasi)
- [🧠 Training Model](#-training-model)
- [🚀 Cara Penggunaan](#-cara-penggunaan)
- [🔌 API Endpoints](#-api-endpoints)
- [☁️ Integrasi Google Drive](#️-integrasi-google-drive-riwayat-prediksi)
- [📈 Hasil Pelatihan Model](#-hasil-pelatihan-model)
- [🚢 Deploy](#-deploy)
- [👨‍💻 Tim Pengembang](#-tim-pengembang)
- [📜 Lisensi](#-lisensi)

---

# 📖 Gambaran Umum

SmartWaste AI adalah aplikasi web berbasis Artificial Intelligence yang membantu pengguna mengenali dan memilah sampah secara otomatis menggunakan Computer Vision dan Deep Learning.

Sistem ini menggabungkan **dua model AI** untuk dua skenario berbeda:

| Mode | Model | Cara Kerja |
|------|-------|------------|
| 📸 **Klasifikasi Gambar** | MobileNetV2 (Keras/TensorFlow) | Pengguna mengunggah foto sampah → model mengklasifikasikan ke 5 kategori |
| 📷 **Deteksi Real-Time** | YOLOv8m (Ultralytics/PyTorch) | Kamera streaming langsung → deteksi objek sampah dengan bounding box & confidence score |

Setiap gambar yang diklasifikasikan melalui halaman Klasifikasi otomatis diupload ke **Google Drive** (berjalan di background thread, tidak menunda response) dan dicatat di `riwayat.jsonl` sebagai log riwayat prediksi.

---

# 🌍 Latar Belakang

Permasalahan sampah masih menjadi salah satu tantangan lingkungan terbesar di Indonesia. Kurangnya kesadaran masyarakat dalam memilah sampah menyebabkan:

- Rendahnya efektivitas proses daur ulang
- Meningkatnya jumlah sampah di Tempat Pembuangan Akhir (TPA)
- Menurunnya efisiensi pengelolaan limbah

SmartWaste AI dikembangkan sebagai solusi edukatif berbasis AI untuk membantu masyarakat mengenali jenis sampah secara cepat dan akurat, sekaligus memberikan rekomendasi pengelolaan yang tepat.

---

# ✨ Fitur Utama

- **Klasifikasi gambar** dengan MobileNetV2 — upload foto dan dapatkan prediksi + confidence score + rekomendasi pengelolaan
- **Deteksi sampah real-time** via webcam dengan YOLOv8m — bounding box, confidence score, dan label kelas langsung di stream video
- **Smoothing deteksi** berbasis voting (deque + Counter) untuk mengurangi flickering label pada mode kamera
- **Rekomendasi pengelolaan** per kategori: tips daur ulang, kompos, pengepul, dll.
- **Integrasi Google Drive** — setiap prediksi otomatis dibackup ke Drive (async, tidak blokir response)
- **Log riwayat prediksi** di `riwayat.jsonl` (prediction, confidence, timestamp, link Drive)
- **Deteksi GPU otomatis** — YOLO pakai GPU (CUDA) jika tersedia, fallback CPU jika tidak
- **Validasi file server-side** — tipe & ukuran file divalidasi di backend (bukan hanya di JS)
- **Frontend modern React + TypeScript** — UI responsif, komponen modular, dan pengalaman pengguna yang cepat dengan Vite

---

# 🧠 Model Artificial Intelligence

## MobileNetV2 — Klasifikasi Gambar

| Properti | Detail |
|----------|--------|
| Arsitektur | MobileNetV2 (Transfer Learning dari ImageNet) |
| Framework | TensorFlow / Keras |
| Input | 224×224 px, 3 channel (RGB) |
| Output | 5 kelas (softmax) |
| File model | `model/classification/smartwaste_mobilenetv2.keras` |
| Training | 2 tahap: head training (15 epoch) + fine-tune top 40 layers (20 epoch) |
| Augmentasi | Rotasi, flip, zoom, brightness, shear |

## YOLOv8m — Deteksi Real-Time

| Properti | Detail |
|----------|--------|
| Arsitektur | YOLOv8 Medium (yolov8m.pt) |
| Framework | Ultralytics / PyTorch |
| Input | 640×640 px |
| Output | 5 kelas + bounding box + confidence |
| File model | `model/yolo/smartwaste_yolo.pt` |
| Training | 100 epoch (dengan resume di Google Colab, GPU Tesla T4), best checkpoint epoch 77 |
| Batch size | 16 (turunkan ke 8/4 jika VRAM < 6GB) |

---

# 🗂 Kategori Sampah

Kedua model menggunakan **5 kelas yang sama**:

| Kategori | Emoji | Warna UI | Penanganan |
|----------|-------|----------|------------|
| Kaca | 🪟 | Ungu `#8b5cf6` | Pisahkan khusus, bungkus pecahan dengan kertas tebal |
| Kertas | 📄 | Kuning `#f59e0b` | Daur ulang / kompos (jika terkena minyak) |
| Logam | ⚙️ | Hijau `#22c55e` | Jual ke pengepul atau bank sampah |
| Organik | 🌿 | Lime `#84cc16` | Kompos |
| Plastik | ♻️ | Cyan `#06b6d4` | Daur ulang, cuci sebelum dibuang |

---

# 📊 Dataset

## Dataset 1 — Klasifikasi Gambar (MobileNetV2)

| Properti | Detail |
|----------|--------|
| Sumber | [Garbage Classification — Mostafa Abla (Kaggle)](https://www.kaggle.com/datasets/mostafaabla/garbage-classification) |
| Kelas asli | 12 kelas (brown-glass, green-glass, white-glass, metal, battery, paper, cardboard, plastic, biological, clothes, shoes, trash) |
| Kelas setelah remap | 5 kelas (Kaca, Kertas, Logam, Organik, Plastik) |
| Format | Folder per kelas (image classification) |
| Ukuran input | Di-resize ke 224×224 px saat preprocessing |
| Script preprocessing | `train/prepare_dataset.py` |

**Mapping kelas (12 → 5):**

| Kelas Asli | → | Kelas SmartWaste |
|------------|---|-----------------|
| brown-glass, green-glass, white-glass, glass | → | Kaca |
| metal, battery, tin | → | Logam |
| paper, cardboard | → | Kertas |
| plastic | → | Plastik |
| biological, organic, food | → | Organik |
| clothes, shoes, trash | → | *(dibuang / tidak digunakan)* |

> ⚠️ Kelas `clothes`, `shoes`, dan `trash` **tidak disertakan** dalam training. Menyertakannya akan menghasilkan 6 kelas yang tidak cocok dengan `CLASS_NAMES_KERAS` di `backend/app.py` (silent bug).

---

## Dataset 2 — Deteksi Objek (YOLOv8m)

| Properti | Detail |
|----------|--------|
| Sumber | [Garbage Classification 3 — Roboflow Universe](https://universe.roboflow.com/material-identification/garbage-classification-3/dataset/2) |
| Lisensi | CC BY 4.0 |
| Jumlah gambar | 10.464 gambar |
| Kelas asli | 6 kelas (BIODEGRADABLE, CARDBOARD, GLASS, METAL, PAPER, PLASTIC) |
| Kelas setelah remap | 5 kelas (kaca, kertas, logam, organik, plastik) |
| Format anotasi | YOLOv8 (YOLO .txt per gambar) |
| Total anotasi dipakai | 74.090 bounding box |
| Preprocessing (Roboflow) | Resize 416×416, auto-orientation, augmentasi flip & rotasi 90° |

**Mapping kelas (6 → 5):**

| Kelas Asli (Roboflow) | → | Kelas SmartWaste |
|-----------------------|---|-----------------|
| BIODEGRADABLE | → | organik |
| CARDBOARD | → | kertas |
| GLASS | → | kaca |
| METAL | → | logam |
| PAPER | → | kertas |
| PLASTIC | → | plastik |
| CLOTH | → | *(dibuang / tidak digunakan)* |

> `CARDBOARD` dan `PAPER` digabung menjadi satu kelas `kertas`. Kelas `CLOTH` dibuang karena tidak relevan.

---

# 🏗 Arsitektur Sistem

Proyek ini menggunakan arsitektur **frontend-backend terpisah** (decoupled):

```
Frontend (React + Vite, port 3000)
  │
  ├── /                      → Home Page
  ├── /klasifikasi           → Upload gambar → POST /api/predict
  │                              ├── MobileNetV2 inference (TF/Keras)
  │                              ├── upload_to_drive_async() [background thread]
  │                              └── append riwayat.jsonl
  ├── /camera                → WebRTC stream → POST /api/camera-frame
  │                              └── YOLOv8m inference (PyTorch/Ultralytics)
  └── /about                 → About Page

  ↕ HTTP (JSON / multipart) — via VITE_API_URL

Backend (Flask, port 5000)
  ├── POST /api/predict          ← multipart/form-data (gambar)
  ├── POST /api/camera-frame     ← JSON {image: base64}
  ├── GET  /api/status           ← status model
  └── GET  /api/health           ← health check
```

Frontend berkomunikasi dengan backend melalui REST API. CORS diaktifkan di backend (`flask-cors`) agar request lintas origin dari frontend dev server dapat diterima.

---

# 💻 Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Frontend | React 19, TypeScript 5.8, Vite 6, react-router-dom v7 |
| Backend | Python 3.11+, Flask 3.0, flask-cors |
| AI — Klasifikasi | TensorFlow 2.13+, Keras, MobileNetV2 |
| AI — Deteksi | PyTorch (CUDA 12.8 / CPU), Ultralytics YOLOv8m |
| Computer Vision | OpenCV 4.8+ |
| Kamera | WebRTC API (browser-native) |
| Storage | Google Drive API v3 (OAuth 2.0) |
| Deployment Frontend | Vercel |
| Deployment Backend | Render / Railway (rekomendasi) |

---

# 📁 Struktur Proyek

```
smartwaste_ai/
├── frontend/                          # React + Vite frontend (TypeScript)
│   ├── index.html                     # Entry HTML (Google Fonts, favicon)
│   ├── package.json                   # Dependencies (react, react-router-dom, vite)
│   ├── vite.config.ts                 # Vite config (port 3000)
│   ├── tsconfig.json                  # TypeScript config
│   ├── vercel.json                    # Vercel routing + API proxy
│   ├── .env.example                   # Template env (VITE_API_URL)
│   ├── public/
│   │   └── images/                    # Aset gambar (logo institusi)
│   └── src/
│       ├── main.tsx                   # Entry point (ReactDOM, BrowserRouter)
│       ├── App.tsx                    # Route definitions
│       ├── components/
│       │   ├── layout/                # Navbar, Footer, Layout, BackgroundOrnaments
│       │   ├── home/                  # StatsBar, FeaturesGrid, HowItWorks, WasteCategories
│       │   └── klasifikasi/           # UploadPanel, ResultsPanel, TipsRow
│       ├── hooks/
│       │   └── useCamera.ts           # WebRTC + real-time detection hook
│       ├── lib/
│       │   ├── api.ts                 # API client (predict, cameraFrame, getStatus)
│       │   ├── constants.ts           # CLASS_NAMES, COLORS, RECOMMENDATIONS
│       │   └── icons.tsx              # EmojiToIcon, SVG icon components
│       ├── pages/
│       │   ├── Home.tsx               # Home Page
│       │   ├── Klasifikasi.tsx        # Classification Page
│       │   ├── Camera.tsx             # Real-Time Camera Page
│       │   └── About.tsx              # About Page
│       └── styles/
│           └── globals.css            # Seluruh styling (ported dari static/css/style.css)
│
├── backend/                           # Flask backend (API only)
│   ├── app.py                         # Flask app (routing, inference, log)
│   ├── drive_storage.py               # Upload async ke Google Drive (background thread)
│   ├── auth_setup.py                  # Generate token.json OAuth Google Drive
│   ├── requirements.txt               # Dependencies GPU (CUDA 12.8)
│   └── requirements-cpu.txt           # Dependencies CPU-only
│
├── model/                             # Model AI (shared oleh backend)
│   ├── classification/
│   │   ├── smartwaste_mobilenetv2.keras   # MobileNetV2 (5 kelas)
│   │   └── class_indices.json             # Mapping index → nama kelas Keras
│   └── yolo/
│       ├── smartwaste_yolo.pt             # YOLOv8m (5 kelas, hasil remap)
│       ├── data.yaml                      # Konfigurasi dataset YOLO
│       ├── dataset.txt                    # Ringkasan mapping & statistik dataset
│       ├── README.dataset.txt             # Dokumentasi dataset asli (Roboflow)
│       └── README.roboflow.txt            # Info ekspor Roboflow
│
├── train/                             # Script training model
│   ├── prepare_dataset.py             # Preprocessing & remap dataset Kaggle (12 → 5)
│   ├── train_keras.py                 # Training MobileNetV2 (2 tahap)
│   ├── train_yolo.py                  # Training YOLOv8m (100 epoch, resume support)
│   ├── evaluate_keras.py              # Evaluasi model Keras (classification report)
│   └── cek_model.py                   # Verifikasi model (cek path & kelas)
│
├── reports/                           # Laporan & grafik pelatihan
│   ├── mobilenet/
│   │   ├── confusion_matrix.png
│   │   └── training_history.png
│   └── yolov8/
│       ├── confusion_matrix_20260619_1412.png
│       ├── confusion_matrix_normalized_20260619_1412.png
│       └── training_history_20260619_1412.png
│
├── riwayat.jsonl                      # Log riwayat prediksi + link Drive (auto-generated)
├── credentials.json                   # OAuth client secret Google (⚠️ jangan commit)
├── token.json                         # OAuth token Google Drive (⚠️ jangan commit)
├── LICENSE
└── README.md
```

> **Catatan:** Folder `static/`, `templates/`, `app.py`, `drive_storage.py`, `auth_setup.py`, `requirements*.txt` di root adalah **legacy code** sebelum migrasi ke arsitektur terpisah dan dapat dihapus atau diabaikan.

---

# ⚙️ Instalasi

## Prasyarat

- Python 3.11+
- Node.js 18+ (untuk frontend)
- Git
- (Opsional) GPU NVIDIA dengan CUDA 12.8 untuk performa YOLO optimal

## Langkah Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/arasyfathi/SmartWaste-AI.git
cd SmartWaste-AI
```

### 2. Setup Backend

```bash
cd backend
```

```bash
# 2a. Install dependencies — jika punya GPU NVIDIA RTX (CUDA 12.8)
pip install -r requirements.txt

# 2b. Install dependencies — CPU only (tanpa GPU NVIDIA)
pip install -r requirements-cpu.txt
```

> ⚠️ `requirements.txt` menggunakan build PyTorch khusus `cu128` untuk NVIDIA Blackwell (RTX 5060+). Jika dijalankan di mesin lain, gunakan `requirements-cpu.txt`.

```bash
# Verifikasi CUDA (opsional, hanya jika install requirements.txt)
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
# Output yang diharapkan: 2.11.0+cu128 True
```

```bash
# Setup Google Drive OAuth (wajib, hanya sekali)
# Letakkan credentials.json dari Google Cloud Console di folder backend/, lalu:
python auth_setup.py
# Browser akan terbuka untuk login Google → menghasilkan token.json di folder backend/
```

```bash
# Jalankan backend
python app.py
```

Backend akan berjalan di:

```
http://localhost:5000
```

### 3. Setup Frontend

Buka terminal baru (jangan tutup terminal backend):

```bash
cd frontend
npm install
```

```bash
# (Opsional) Buat file .env jika backend berjalan di URL berbeda
cp .env.example .env
# Edit VITE_API_URL jika perlu (default: http://localhost:5000)
```

```bash
# Jalankan frontend dev server
npm run dev
```

Frontend akan berjalan di:

```
http://localhost:3000
```

---

# 🧠 Training Model

> Model sudah tersedia di folder `model/`. Bagian ini hanya diperlukan jika ingin melatih ulang dari awal.

## A. MobileNetV2 — Klasifikasi Gambar

**1. Download Dataset dari Kaggle:**

- Dataset: [Garbage Classification — Mostafa Abla](https://www.kaggle.com/datasets/mostafaabla/garbage-classification)
- Ekstrak ke folder `datasets/raw/`

**2. Preprocessing & remap kelas (12 → 5):**

```bash
python train/prepare_dataset.py --src datasets/raw --dst datasets/garbage
```

Script ini melakukan resize gambar ke 224×224 px, memetakan 12 kelas asli ke 5 kelas SmartWaste AI, dan membuang kelas yang tidak relevan (`clothes`, `shoes`, `trash`).

**3. Training (2 tahap):**

```bash
python train/train_keras.py
```

- **Tahap 1** (15 epoch): Training head baru dengan base frozen
- **Tahap 2** (20 epoch): Fine-tune top 40 layers dengan learning rate rendah (5e-6)

Output: `model/classification/smartwaste_mobilenetv2.keras` dan `model/classification/class_indices.json`

---

## B. YOLOv8m — Deteksi Real-Time

**1. Download Dataset dari Roboflow:**

- Dataset: [Garbage Classification 3 — v2 GC1](https://universe.roboflow.com/material-identification/garbage-classification-3/dataset/2)
- Format: YOLOv8, ekspor ke `datasets/garbage-classification-3/`

**2. Remap kelas (6 → 5) dan buat `data.yaml`:**

Setelah remap, `data.yaml` berisi:

```yaml
nc: 5
names: ['kaca', 'kertas', 'logam', 'organik', 'plastik']
train: datasets/dataset_remapped/train/images
val:   datasets/dataset_remapped/valid/images
test:  datasets/dataset_remapped/test/images
```

Detail mapping lengkap ada di `model/yolo/dataset.txt`.

**3. Training (YOLOv8m, 100 epoch):**

```bash
python train/train_yolo.py
```

Training dilakukan di Google Colab (GPU Tesla T4). Checkpoint disimpan setiap 10 epoch (`save_period=10`) sebagai antisipasi putus koneksi.

Output: `model/yolo/smartwaste_yolo.pt` (di-copy dari `runs/detect/smartwaste_yolov8m/weights/best.pt`)

---

# 🚀 Cara Penggunaan

## Klasifikasi Gambar

1. Buka halaman **Klasifikasi** (`/klasifikasi`) di frontend
2. Upload foto sampah (JPG, PNG, WebP, maks 10MB)
3. Klik **Prediksi**
4. Lihat hasil: kategori, confidence score per kelas, dan rekomendasi pengelolaan

## Deteksi Real-Time

1. Buka halaman **Camera** (`/camera`) di frontend
2. Izinkan akses webcam di browser
3. Arahkan kamera ke objek sampah
4. Sistem mendeteksi secara real-time dengan bounding box, label, dan confidence score

---

# 🔌 API Endpoints

Semua endpoint berada di **backend** (`http://localhost:5000`). Frontend mengaksesnya melalui API client di `frontend/src/lib/api.ts`.

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/predict` | Prediksi gambar (multipart/form-data) |
| POST | `/api/camera-frame` | Deteksi satu frame (JSON base64) |
| GET | `/api/status` | Status model yang dimuat |
| GET | `/api/health` | Health check backend |

### Contoh: POST `/api/predict`

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
    "tips": [
      "Pisahkan ke tempat sampah daur ulang plastik (biasanya berwarna kuning).",
      "Cuci dan keringkan sebelum dibuang agar tidak terkontaminasi.",
      "..."
    ]
  }
}
```

### Contoh: POST `/api/camera-frame`

```bash
curl -X POST http://localhost:5000/api/camera-frame \
  -H "Content-Type: application/json" \
  -d '{"image": "<base64-encoded-frame>"}'
```

---

# ☁️ Integrasi Google Drive (Riwayat Prediksi)

Setiap kali endpoint `/api/predict` dipanggil, gambar yang diupload otomatis dikirim ke Google Drive melalui `backend/drive_storage.py`. Proses ini berjalan di **background thread** agar tidak menunda response API. Hasilnya (`prediction`, `confidence`, link Drive) dicatat sebagai satu baris JSON di `riwayat.jsonl`.

**Setup OAuth (sekali saja, sebelum pertama kali jalan):**

```bash
cd backend
python auth_setup.py
```

Script ini membuka browser untuk login Google, lalu menghasilkan `token.json` yang dipakai otomatis oleh `drive_storage.py` (termasuk auto-refresh token).

**Yang diperlukan:**

- `credentials.json` (OAuth client secret dari Google Cloud Console) — letakkan di folder `backend/`
- (Opsional) Environment variable `DRIVE_FOLDER_ID` untuk menentukan folder tujuan upload

> ⚠️ `credentials.json` dan `token.json` berisi kredensial sensitif — sudah masuk `.gitignore`, **jangan pernah commit** ke repository publik.

---

# 📈 Hasil Pelatihan Model

## MobileNetV2 (Klasifikasi Gambar)

| Metrik | Nilai |
|--------|-------|
| Training Accuracy | 90.02% |
| Validation Accuracy | 93.53% |
| Validation Loss | 0.3274 |

> Grafik training history dan confusion matrix tersedia di `reports/mobilenet/`.

---

## YOLOv8m (Deteksi Real-Time)

Training 100 epoch di Google Colab (GPU Tesla T4), best checkpoint di epoch 77.

**Metrik keseluruhan:**

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

> **Catatan:**
> - Kelas **Plastik** memiliki performa terendah, kemungkinan akibat class imbalance (jumlah instance jauh lebih sedikit dari kelas lain).
> - Kelas **Organik** cukup sering tertukar dengan background pada confusion matrix, kemungkinan akibat dominasi jumlah instance Organik di dataset.
> - Grafik training history dan confusion matrix (raw & normalized) tersedia di `reports/yolov8/`.

---

# 🚢 Deploy

## Frontend → Vercel

Frontend React dapat di-deploy langsung ke Vercel:

```bash
cd frontend
npm run build        # Output ke frontend/dist/
```

File `frontend/vercel.json` sudah dikonfigurasi untuk:
- Routing SPA (fallback ke `index.html` untuk react-router-dom)
- API proxy dari `/api/*` ke backend

Setelah deploy, update URL proxy di `vercel.json` agar mengarah ke URL backend produksi (bukan `localhost:5000`).

## Backend → Render / Railway

Backend Flask perlu di-deploy ke platform yang mendukung Python + TensorFlow/YOLO:

```bash
# Build command:
pip install -r requirements-cpu.txt

# Start command:
gunicorn app:app
```

> Tambahkan `gunicorn` ke `requirements.txt` jika belum ada.

Render/Railway akan memberikan URL publik (`https://nama-app.onrender.com`). Gunakan URL ini sebagai nilai `VITE_API_URL` di environment variable Vercel frontend, dan juga update `vercel.json` proxy destination.

---

# 👨‍💻 Tim Pengembang

| Nama | NIM | Peran |
|------|-----|-------|
| **Fathi Arasy** | 101022400103 | Machine Learning & Backend Developer |
| **Adelia Afriliani** | 101052300002 | UI/UX Designer & Frontend Developer |
| **Ghalib Hafuza** | 10012400211 | Computer Vision & Model Development |

**Telkom University — Tahun Akademik 2026**

---

# 📜 Lisensi

Proyek ini dikembangkan untuk keperluan akademik sebagai bagian dari Proyek IMV di Telkom University.

© 2026 SmartWaste AI Team
