"""
prepare_dataset.py — Persiapan & preprocessing dataset SmartWaste AI
Dataset: Garbage Classification (Mostafa Abla) - 12 kelas
"""

import os
import argparse
import shutil
from pathlib import Path
import cv2
from tqdm import tqdm

# Mapping 12 kelas Mostafa Abla → 5 kelas SmartWaste AI
LABEL_MAP = {
    # Kaca
    'brown-glass':  'Kaca',
    'green-glass':  'Kaca',
    'white-glass':  'Kaca',
    'glass':        'Kaca',
    # Logam
    'metal':        'Logam',
    'battery':      'Logam',
    'tin':          'Logam',
    # Kertas
    'paper':        'Kertas',
    'cardboard':    'Kertas',
    # Plastik
    'plastic':      'Plastik',
    # Organik / Lainnya
    'biological':   'Organik',
    'organic':      'Organik',
    'food':         'Organik',
    # Dibuang / tidak dipakai → masuk Lainnya (opsional)
    'clothes':      'Lainnya',
    'shoes':        'Lainnya',
    'trash':        'Lainnya',
    # Sudah Indonesia
    'Plastik':  'Plastik',
    'Kertas':   'Kertas',
    'Kaca':     'Kaca',
    'Logam':    'Logam',
    'Organik':  'Organik',
    'Lainnya':  'Lainnya',
}

VALID_EXT = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
TARGET_SIZE = (224, 224)


def validate_image(path):
    try:
        img = cv2.imread(str(path))
        return img is not None and img.shape[0] > 0 and img.shape[1] > 0
    except:
        return False


def process_dataset(src_dir, dst_dir, resize=True, include_lainnya=False):
    src = Path(src_dir)
    dst = Path(dst_dir)

    if not src.exists():
        print(f"[ERROR] Folder sumber tidak ada: {src}")
        return

    stats = {}
    skipped = 0
    unrecognized = []
    excluded_lainnya = 0

    for folder in sorted(src.iterdir()):
        if not folder.is_dir():
            continue

        label = LABEL_MAP.get(folder.name)
        if not label:
            unrecognized.append(folder.name)
            print(f"[SKIP] Folder tidak dikenali: {folder.name}")
            continue

        # PENTING: app.py & model klasifikasi HARDCODE 5 kelas (Kaca, Kertas,
        # Logam, Organik, Plastik). Kalau folder "Lainnya" ikut ditulis ke
        # dst_dir, train_keras.py akan otomatis mendeteksi 6 kelas (lewat
        # os.listdir), dan index kelas hasil training TIDAK AKAN COCOK lagi
        # dengan urutan CLASS_NAMES_KERAS di app.py — model akan salah label
        # tanpa error apa pun (silent bug). Default: kelas ini DISKIP.
        # Gunakan --include-lainnya hanya jika app.py & CLASS_NAMES_KERAS juga
        # sudah diupdate untuk mendukung 6 kelas.
        if label == 'Lainnya' and not include_lainnya:
            excluded_lainnya += len([f for f in folder.iterdir() if f.suffix.lower() in VALID_EXT])
            print(f"[SKIP] {folder.name} → 'Lainnya' diabaikan (pakai --include-lainnya untuk menyertakan)")
            continue

        out_dir = dst / label
        out_dir.mkdir(parents=True, exist_ok=True)

        images = [f for f in folder.iterdir() if f.suffix.lower() in VALID_EXT]
        print(f"\n[>] {folder.name} → {label} ({len(images)} gambar)")

        count = 0
        for img_path in tqdm(images, desc=label):
            if not validate_image(img_path):
                skipped += 1
                continue

            # Tambahkan prefix nama folder agar tidak ada konflik nama file
            out_name = f"{folder.name}_{img_path.name}"
            if resize:
                img = cv2.imread(str(img_path))
                img = cv2.resize(img, TARGET_SIZE, interpolation=cv2.INTER_LANCZOS4)
                cv2.imwrite(str(out_dir / out_name), img)
            else:
                shutil.copy(img_path, out_dir / out_name)
            count += 1

        stats[label] = stats.get(label, 0) + count

    print("\n" + "=" * 50)
    print("STATISTIK DATASET")
    print("=" * 50)
    total = 0
    for label, count in sorted(stats.items()):
        print(f"  {label:12s}: {count:6,} gambar")
        total += count
    print(f"  {'TOTAL':12s}: {total:6,} gambar")
    print(f"  Dilewati (rusak)   : {skipped}")
    if excluded_lainnya:
        print(f"  Dikecualikan (Lainnya): {excluded_lainnya} gambar (tidak ditulis ke {dst_dir})")
    if unrecognized:
        print(f"  Tidak dikenali : {unrecognized}")
    n_classes = len(stats)
    print(f"\nJumlah kelas final di {dst_dir}: {n_classes}", "✓ (sesuai 5 kelas app.py)" if n_classes == 5 else "⚠ BUKAN 5 — cek app.py & CLASS_NAMES_KERAS sebelum training!")
    print(f"Output tersimpan di: {dst_dir}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Persiapan dataset SmartWaste AI')
    parser.add_argument('--src', default='datasets/raw',   help='Folder dataset mentah')
    parser.add_argument('--dst', default='datasets/garbage', help='Folder output')
    parser.add_argument('--no-resize', action='store_true', help='Jangan resize gambar')
    parser.add_argument('--include-lainnya', action='store_true',
                         help='Sertakan kelas "Lainnya" (clothes/shoes/trash) — '
                              'JANGAN dipakai kecuali app.py & CLASS_NAMES_KERAS '
                              'sudah diupdate untuk 6 kelas.')
    args = parser.parse_args()

    process_dataset(args.src, args.dst, resize=not args.no_resize,
                     include_lainnya=args.include_lainnya)