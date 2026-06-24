# Catatan Deploy SmartWaste AI — 23 Juni 2026

## Ringkasan

Sesi ini mencakup penulisan ulang README, deployment frontend ke **Vercel**, deployment backend ke **Hugging Face Spaces** (Docker), serta perbaikan berbagai bug yang muncul selama proses deploy.

---

## 1. Penulisan Ulang README

README.md ditulis ulang untuk mencerminkan arsitektur baru (frontend-backend terpisah):

- Menambahkan badge React, TypeScript, Vite
- Diagram arsitektur diperbarui (frontend React ↔ backend Flask via REST API)
- Tech Stack table diperbarui (React 19, TypeScript 5.8, Vite 6, react-router-dom v7)
- Struktur proyek diperbarui dengan direktori `frontend/` dan `backend/`
- Panduan instalasi dipisah menjadi setup Backend dan Frontend
- Section Deploy: Vercel untuk frontend, Render/Railway untuk backend

**Commit:** `feat: migrate to React + Flask separated architecture`

---

## 2. Fix Build Error Vercel (TypeScript)

### Error

```
src/components/home/StatsBar.tsx(1,29): error TS6133: 'useState' is declared but its value is never read.
src/components/home/StatsBar.tsx(40,13): error TS2349: This expression is not callable.
src/components/klasifikasi/ResultsPanel.tsx(3,21): error TS6133: 'RecycleIcon' is declared but its value is never read.
src/components/klasifikasi/ResultsPanel.tsx(105,44): error TS6133: 'icon' is declared but its value is never read.
```

### Perbaikan

| File | Masalah | Fix |
|------|---------|-----|
| `StatsBar.tsx` | `useState` dipanggil tanpa wrapper `useState()` | `const [display, setDisplay] = useState(...)` |
| `ResultsPanel.tsx` | Import `RecycleIcon` tidak dipakai | Hapus dari import |
| `ResultsPanel.tsx` | Prop `icon` di `ConfidenceRow` tidak dipakai | Hapus dari interface dan call site |

**Commit:** `fix: resolve TypeScript build errors in StatsBar and ResultsPanel`

---

## 3. Konten Halaman Tidak Muncul (Klasifikasi, Camera, About)

### Masalah

Halaman Klasifikasi, Camera, dan About hanya menampilkan judul (page-hero) tanpa konten di bawahnya.

### Root Cause

CSS class `.fade-up` mengatur `opacity: 0` dan menunggu class `.visible` ditambahkan oleh IntersectionObserver. Di halaman Home, komponen `<ScrollReveal>` menangani ini. Tapi di halaman lain, class `.fade-up` dipakai langsung tanpa observer — sehingga konten tetap invisible.

### Perbaikan

Menambahkan global IntersectionObserver di `Layout.tsx` yang:
1. Observe semua elemen `.fade-up` yang ada saat mount
2. Menggunakan MutationObserver untuk mendeteksi elemen `.fade-up` baru yang ditambahkan saat navigasi SPA (route change)

```tsx
// Layout.tsx — useEffect
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-up').forEach((el) => observer.observe(el));

// + MutationObserver untuk elemen baru saat route change
```

**Commit:** `fix: add global IntersectionObserver for .fade-up elements on all pages`

---

## 4. Konfigurasi Docker untuk Hugging Face Spaces

### File yang Dibuat

| File | Fungsi |
|------|--------|
| `Dockerfile` | Python 3.11-slim, port 7860, gunicorn (1 worker, 4 threads, 120s timeout) |
| `hf_requirements.txt` | CPU-only PyTorch, tensorflow-cpu, opencv-python-headless, flask-cors |

### Perubahan di `app.py`

1. **Model paths fleksibel** — cek multiple lokasi (`../model/`, `./model/`, `cwd/model/`) supaya jalan di local dev dan Docker
2. **Google Drive opsional** — import `drive_storage` di-wrap try/except, prediksi tetap jalan tanpa Drive
3. **`drive_storage.py`** — cek `token.json` sebelum upload, skip gracefully jika tidak ada

**Commit:** `feat: add Docker configuration for Hugging Face Spaces deployment`

---

## 5. Deploy ke Hugging Face Spaces

### Langkah yang Dilakukan

1. Buat Space baru di HF: SDK = **Docker**, nama = `smartwaste`
2. Clone HF Space repo ke `frontend/smartwaste/`
3. Copy backend files (`backend/*.py`), `Dockerfile`, `hf_requirements.txt`, dan model files
4. Setup Git LFS untuk track `*.keras` dan `*.pt`
5. Commit & push ke HF

### Masalah yang Dihadapi

| Masalah | Solusi |
|---------|--------|
| Password auth tidak didukung HF | Gunakan **User Access Token** (scope: Write) di remote URL |
| Model files tidak ter-push (gitignored `*.keras`, `*.pt`) | Gunakan `git lfs track` lalu push ulang |
| `Copy-Item` tidak dikenali di CMD | Gunakan `copy` (CMD) bukan `Copy-Item` (PowerShell) |

### URL Backend

```
https://fathiarasy-smartwaste.hf.space
```

---

## 6. Update Frontend (Vercel) ke HF Backend

### Perubahan

`frontend/vercel.json` — API proxy destination diubah:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://fathiarasy-smartwaste.hf.space/api/:path*"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

**Commit:** `chore: update API proxy to Hugging Face Spaces backend`

---

## 7. Bug: Model Tidak Ter-load di HF Spaces

### Gejala

`/api/status` menampilkan:
```json
{"keras_loaded": false, "yolo_loaded": false}
```

`/api/debug` menampilkan `{}` (kosong).

### Root Cause

`load_models()` dan `warmup_models()` hanya dipanggil di dalam blok:

```python
if __name__ == '__main__':
    load_models()
    warmup_models()
```

Gunicorn **mengimport** module `app:app`, bukan menjalankannya langsung. Jadi `__name__` adalah `'app'` bukan `'__main__'`, dan model tidak pernah di-load.

### Perbaikan

Pindahkan `load_models()` dan `warmup_models()` ke **module level** (di luar `if __name__`):

```python
# Load models at import time (needed for gunicorn / production servers)
load_models()
warmup_models()

if __name__ == '__main__':
    app.run(...)
```

### Endpoint Debug

Ditambahkan `/api/debug` yang menampilkan info diagnostik:
- `model_dir`, `model_dir_exists`, `model_dir_contents`
- `keras_path`, `keras_exists`, `keras_status`, `keras_error`
- `yolo_candidates`, `yolo_exists`, `yolo_status`, `yolo_error`
- `tf_version`

**Commit:** `fix: load models at import time for gunicorn/HF Spaces`

---

## 8. Tambahan: Embedded Git Repository

### Masalah

Folder `frontend/smartwaste/` (HF Space clone) memiliki `.git/` sendiri, sehingga terdeteksi sebagai embedded git repo saat `git add`.

### Solusi

```bash
git rm --cached frontend/smartwaste
```

Tambahkan ke `.gitignore`:
```
frontend/smartwaste/
```

---

## Arsitektur Final

```
User
  │
  ├──→ Vercel (React Frontend)
  │       Port: 443 (HTTPS)
  │       Routes: /, /klasifikasi, /camera, /about
  │
  │       /api/* ──proxy──→ Hugging Face Spaces (Flask Backend)
  │                              Port: 7860 (Docker)
  │                              Models: MobileNetV2 + YOLOv8m (CPU)
  │                              Server: Gunicorn (1 worker, 4 threads)
  │
  └──→ GitHub (Source Code)
          repo: arasyfathi/SmartWaste-AI
```

---

## Checklist Status

| Item | Status |
|------|--------|
| Frontend (Vercel) | Deployed |
| Backend (HF Spaces) | Deployed, models need verification |
| API Proxy (Vercel → HF) | Configured |
| Klasifikasi (MobileNetV2) | Pending verification |
| Camera Real-time (YOLOv8m) | Pending verification |
| Google Drive Integration | Disabled (no token.json in Docker) |

---

## Daftar Commit (Sesi Ini)

| Commit | Deskripsi |
|--------|-----------|
| `0fcbf217` | feat: migrate to React + Flask separated architecture |
| `3d667e45` | fix: resolve TypeScript build errors in StatsBar and ResultsPanel |
| `0cd38fd9` | fix: add global IntersectionObserver for .fade-up elements on all pages |
| `6c62d07d` | feat: add Docker configuration for Hugging Face Spaces deployment |
| `78b7acf9` | chore: update API proxy to Hugging Face Spaces backend |
| `f9172b8f` | fix: load models at import time for gunicorn/HF Spaces |
