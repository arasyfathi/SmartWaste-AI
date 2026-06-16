"""
train_yolo.py — Training YOLOv8 untuk SmartWaste AI (Camera Real-Time)

Dataset: Garbage Classification 3 (Roboflow) - 6 kelas
Output : model/smartwaste_yolo.pt

Cara pakai:
  pip install ultralytics
  python train_yolo.py
"""

from ultralytics import YOLO
import os, yaml, shutil
from pathlib import Path

# ── Konfigurasi ───────────────────────────────────────────────────────────────
DATA_YAML   = 'datasets/yolo/data.yaml'
MODEL_OUT   = 'model/smartwaste_yolo.pt'
EPOCHS      = 50
IMG_SIZE    = 640
BATCH_SIZE  = 8      # Turunkan ke 4 jika RAM < 8GB
WORKERS     = 2
PROJECT     = 'runs/detect'
RUN_NAME    = 'smartwaste'

os.makedirs('model', exist_ok=True)

def train():
    print("=" * 60)
    print("  SmartWaste AI — YOLOv8 Training")
    print("=" * 60)

    if not os.path.exists(DATA_YAML):
        print(f"[ERROR] data.yaml tidak ditemukan: {DATA_YAML}")
        return

    # Tampilkan info dataset
    with open(DATA_YAML) as f:
        info = yaml.safe_load(f)
    print(f"\n[✓] Kelas ({info['nc']}): {info['names']}")
    print(f"[✓] Train : {info.get('train')}")
    print(f"[✓] Val   : {info.get('val')}")

    # Load YOLOv8 nano (paling ringan, cocok untuk CPU)
    print("\n[>] Loading YOLOv8n pretrained weights...")
    model = YOLO('yolov8n.pt')

    # Training
    print(f"\n[>] Mulai training {EPOCHS} epoch...")
    results = model.train(
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
        plots     = True,
        verbose   = True,
        device    = 'cpu',      # Ganti ke 0 jika punya GPU NVIDIA
    )

    # Copy model terbaik ke folder model/
    best = Path(PROJECT) / RUN_NAME / 'weights' / 'best.pt'
    if best.exists():
        shutil.copy(best, MODEL_OUT)
        print(f"\n[✓] Model terbaik disimpan: {MODEL_OUT}")
    else:
        print(f"\n[!] best.pt tidak ditemukan di {best}")

    print("\n✅ Training YOLOv8 selesai!")
    print(f"   Cek hasil di: {PROJECT}/{RUN_NAME}/")

if __name__ == '__main__':
    train()