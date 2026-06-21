"""
train_yolo.py — Training YOLOv8m untuk SmartWaste AI (Camera Real-Time)

Dataset: GARBAGE CLASSIFICATION 3 (Roboflow), hasil remap 6 → 5 kelas
         (kaca, kertas, logam, organik, plastik — lihat model/yolo/dataset.txt)
Output : model/yolo/smartwaste_yolo.pt

PENTING: path output HARUS SAMA dengan YOLO_CANDIDATES di app.py
(model/yolo/smartwaste_yolo.pt). Versi script ini sebelumnya menyimpan ke
'model/smartwaste_yolo.pt' (folder lama, sebelum struktur project dipisah
jadi model/classification/ & model/yolo/) — kalau dijalankan ulang tanpa
diedit, model baru tidak akan otomatis terpakai oleh app.py.

Cara pakai:
  pip install ultralytics
  python train_yolo.py
"""

from ultralytics import YOLO
import os, yaml, shutil
from pathlib import Path

try:
    import torch
    DEVICE = 0 if torch.cuda.is_available() else 'cpu'
    if torch.cuda.is_available():
        print(f"[✓] GPU terdeteksi: {torch.cuda.get_device_name(0)} — training pakai GPU")
    else:
        print("[!] GPU tidak terdeteksi — training fallback ke CPU (jauh lebih lambat)")
except ImportError:
    DEVICE = 'cpu'
    print("[!] PyTorch tidak ditemukan — fallback ke CPU")

# ── Konfigurasi ───────────────────────────────────────────────────────────────
# Dataset hasil remap (lihat train/prepare_dataset.py & model/yolo/dataset.txt
# untuk mapping kelas asli Roboflow → 5 kelas Indonesia).
DATA_YAML   = 'datasets/dataset_remapped/data.yaml'
MODEL_OUT   = 'model/yolo/smartwaste_yolo.pt'
BASE_MODEL  = 'yolov8m.pt'   # medium — akurasi lebih baik dari nano, masih layak GPU consumer
EPOCHS      = 100
IMG_SIZE    = 640
BATCH_SIZE  = 16             # Turunkan (8/4) jika VRAM < 6GB
WORKERS     = 4
PROJECT     = 'runs/detect'
RUN_NAME    = 'smartwaste_yolov8m'

os.makedirs('model/yolo', exist_ok=True)


def train():
    print("=" * 60)
    print("  SmartWaste AI — YOLOv8m Training")
    print("=" * 60)

    if not os.path.exists(DATA_YAML):
        print(f"[ERROR] data.yaml tidak ditemukan: {DATA_YAML}")
        print("Pastikan dataset sudah di-remap (lihat README.md bagian Dataset).")
        return

    # Tampilkan info dataset
    with open(DATA_YAML) as f:
        info = yaml.safe_load(f)
    print(f"\n[✓] Kelas ({info['nc']}): {info['names']}")
    print(f"[✓] Train : {info.get('train')}")
    print(f"[✓] Val   : {info.get('val')}")

    if info.get('nc') != 5:
        print(f"\n[!] PERINGATAN: jumlah kelas di data.yaml ({info.get('nc')}) BUKAN 5.")
        print("    YOLO_CLASS_MAP di app.py hardcode 5 kelas — training dengan jumlah")
        print("    kelas lain akan membuat model TIDAK COCOK dengan app.py (silent bug).")

    print(f"\n[>] Loading {BASE_MODEL} pretrained weights...")
    model = YOLO(BASE_MODEL)

    # Training
    print(f"\n[>] Mulai training {EPOCHS} epoch (device={DEVICE})...")
    model.train(
        data      = DATA_YAML,
        epochs    = EPOCHS,
        imgsz     = IMG_SIZE,
        batch     = BATCH_SIZE,
        workers   = WORKERS,
        project   = PROJECT,
        name      = RUN_NAME,
        exist_ok  = True,
        patience  = 15,         # Early stopping
        save      = True,
        save_period = 10,       # checkpoint tiap 10 epoch (jaga-jaga training putus)
        plots     = True,
        verbose   = True,
        device    = DEVICE,
    )

    # Copy model terbaik ke folder model/yolo/
    best = Path(PROJECT) / RUN_NAME / 'weights' / 'best.pt'
    if best.exists():
        shutil.copy(best, MODEL_OUT)
        print(f"\n[✓] Model terbaik disimpan: {MODEL_OUT}")
    else:
        print(f"\n[!] best.pt tidak ditemukan di {best}")

    print("\n✅ Training YOLOv8m selesai!")
    print(f"   Cek hasil & plot di: {PROJECT}/{RUN_NAME}/")


if __name__ == '__main__':
    train()
