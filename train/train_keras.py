"""
train_keras.py — Training MobileNetV2 classifier untuk SmartWaste AI
Dataset: 5 kelas → Kaca, Kertas, Logam, Organik, Plastik

Cara pakai:
  python train_keras.py

Output:
  model/classification/smartwaste_mobilenetv2.keras
  model/classification/class_indices.json
"""

import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard
)

# ─── Konfigurasi ──────────────────────────────────────────────────────────────
DATA_DIR     = 'datasets/garbage'
# PENTING: path & format ini HARUS SAMA dengan MODEL_PATH_KERAS di app.py
# (model/classification/smartwaste_mobilenetv2.keras). Sebelumnya script ini
# menyimpan ke 'model/smartwaste_model.h5' — path & ekstensi berbeda dari yang
# dipakai app.py, sehingga model hasil training ulang TIDAK PERNAH otomatis
# terpakai oleh web app (app.py tetap memuat model lama tanpa ada error).
MODEL_OUTPUT      = 'model/classification/smartwaste_mobilenetv2.keras'
CLASS_INDICES_OUT = 'model/classification/class_indices.json'
IMG_SIZE     = 224
BATCH_SIZE   = 32
EPOCHS_FT1   = 15   # Tahap 1: head only
EPOCHS_FT2   = 20   # Tahap 2: fine-tune top layers
VAL_SPLIT    = 0.2

os.makedirs(os.path.dirname(MODEL_OUTPUT), exist_ok=True)
os.makedirs('logs', exist_ok=True)


def build_model(num_classes):
    base = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    base.trainable = False

    inputs  = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    x = base(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    return Model(inputs, outputs), base


def get_data_generators():
    train_gen = ImageDataGenerator(
        rescale            = 1./255,
        validation_split   = VAL_SPLIT,
        rotation_range     = 25,
        width_shift_range  = 0.15,
        height_shift_range = 0.15,
        horizontal_flip    = True,
        vertical_flip      = False,
        zoom_range         = 0.15,
        brightness_range   = [0.75, 1.25],
        shear_range        = 0.1,
        fill_mode          = 'nearest',
    )
    val_gen = ImageDataGenerator(
        rescale          = 1./255,
        validation_split = VAL_SPLIT,
    )

    train_ds = train_gen.flow_from_directory(
        DATA_DIR,
        target_size = (IMG_SIZE, IMG_SIZE),
        batch_size  = BATCH_SIZE,
        class_mode  = 'categorical',
        subset      = 'training',
        shuffle     = True,
    )
    val_ds = val_gen.flow_from_directory(
        DATA_DIR,
        target_size = (IMG_SIZE, IMG_SIZE),
        batch_size  = BATCH_SIZE,
        class_mode  = 'categorical',
        subset      = 'validation',
        shuffle     = False,
    )
    return train_ds, val_ds


def compute_class_weights(train_ds):
    """Hitung class weights untuk handle imbalance data."""
    from sklearn.utils.class_weight import compute_class_weight
    labels = train_ds.classes
    classes = np.unique(labels)
    weights = compute_class_weight(class_weight='balanced', classes=classes, y=labels)
    return dict(zip(classes, weights))


def train():
    print("=" * 60)
    print("  SmartWaste AI — MobileNetV2 Training")
    print("=" * 60)

    # Cek dataset
    if not os.path.exists(DATA_DIR):
        print(f"\n[ERROR] Folder dataset tidak ditemukan: {DATA_DIR}")
        print("Pastikan sudah menjalankan: python prepare_dataset.py")
        return

    # Cek folder kelas
    kelas = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
    print(f"\n[✓] Kelas ditemukan ({len(kelas)}): {sorted(kelas)}")

    # Load data
    train_ds, val_ds = get_data_generators()
    print(f"[✓] Train : {train_ds.samples} gambar")
    print(f"[✓] Val   : {val_ds.samples} gambar")
    print(f"[✓] Kelas : {train_ds.class_indices}")

    # Class weights (atasi imbalance: Organik 985 vs Kertas 1941)
    try:
        class_weights = compute_class_weights(train_ds)
        print(f"\n[✓] Class weights: { {k: round(v,2) for k,v in class_weights.items()} }")
    except ImportError:
        print("[!] sklearn tidak ada, class weights dinonaktifkan")
        class_weights = None

    # Build model
    model, base = build_model(num_classes=len(train_ds.class_indices))
    model.summary()

    # ── Tahap 1: Train head ───────────────────────────────────────────────────
    print("\n" + "─" * 60)
    print("  TAHAP 1: Training Head (Base Frozen)")
    print("─" * 60)

    model.compile(
        optimizer = tf.keras.optimizers.Adam(1e-3),
        loss      = 'categorical_crossentropy',
        metrics   = ['accuracy']
    )

    cb1 = [
        ModelCheckpoint(MODEL_OUTPUT, save_best_only=True,
                        monitor='val_accuracy', verbose=1),
        EarlyStopping(patience=7, restore_best_weights=True,
                      monitor='val_accuracy', verbose=1),
        ReduceLROnPlateau(factor=0.5, patience=3, verbose=1, min_lr=1e-7),
        TensorBoard(log_dir='logs/stage1'),
    ]

    model.fit(
        train_ds,
        epochs          = EPOCHS_FT1,
        validation_data = val_ds,
        callbacks       = cb1,
        class_weight    = class_weights,
    )

    # ── Tahap 2: Fine-tune top layers ─────────────────────────────────────────
    print("\n" + "─" * 60)
    print("  TAHAP 2: Fine-tuning (Unfreeze Top 40 Layers)")
    print("─" * 60)

    base.trainable = True
    for layer in base.layers[:-40]:
        layer.trainable = False

    model.compile(
        optimizer = tf.keras.optimizers.Adam(5e-6),
        loss      = 'categorical_crossentropy',
        metrics   = ['accuracy']
    )

    cb2 = [
        ModelCheckpoint(MODEL_OUTPUT, save_best_only=True,
                        monitor='val_accuracy', verbose=1),
        EarlyStopping(patience=8, restore_best_weights=True,
                      monitor='val_accuracy', verbose=1),
        ReduceLROnPlateau(factor=0.3, patience=4, verbose=1, min_lr=1e-8),
        TensorBoard(log_dir='logs/stage2'),
    ]

    model.fit(
        train_ds,
        epochs          = EPOCHS_FT2,
        validation_data = val_ds,
        callbacks       = cb2,
        class_weight    = class_weights,
    )

    # ── Evaluasi Akhir ────────────────────────────────────────────────────────
    print("\n" + "─" * 60)
    print("  EVALUASI AKHIR")
    print("─" * 60)

    loss, acc = model.evaluate(val_ds, verbose=1)
    print(f"\n  Validation Loss    : {loss:.4f}")
    print(f"  Validation Accuracy: {acc * 100:.2f}%")

    # Simpan class indices
    with open(CLASS_INDICES_OUT, 'w') as f:
        json.dump(train_ds.class_indices, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] Model disimpan   : {MODEL_OUTPUT}")
    print(f"[✓] Class indices    : {CLASS_INDICES_OUT}")
    print("\n✅ Training selesai!")


if __name__ == '__main__':
    train()