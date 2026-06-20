import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''  # ← tambahkan di sini
import io
import base64
import json
import time
import threading
from collections import deque, defaultdict, Counter
import numpy as np
from flask import Flask, render_template, request, jsonify, Response
from PIL import Image
import cv2

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max upload

# ─── Konfigurasi ──────────────────────────────────────────────────────────────
UPLOAD_FOLDER    = 'static/uploads'
MODEL_PATH_KERAS = 'model/classification/smartwaste_mobilenetv2.keras'
IMG_SIZE         = 224

# Path YOLO: cek hasil training baru dulu, fallback ke model lama
YOLO_CANDIDATES = [
    'model/yolo/smartwaste_yolo.pt',
    'model/smartwaste_yolo.pt'
]
MODEL_PATH_YOLO = next((p for p in YOLO_CANDIDATES if os.path.exists(p)), None)

# Kelas Keras (5 kelas Indonesia)
CLASS_NAMES_KERAS = ['Kaca', 'Kertas', 'Logam', 'Organik', 'Plastik']

# Kelas YOLO (5 kelas, hasil remap dataset Roboflow 6→5) → mapping ke nama Indonesia
# Urutan sesuai data.yaml hasil remap: kaca, kertas, logam, organik, plastik (alfabetis)
YOLO_CLASS_MAP = {
    0: 'Kaca',
    1: 'Kertas',
    2: 'Logam',
    3: 'Organik',
    4: 'Plastik',
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ─── Rekomendasi per kategori ─────────────────────────────────────────────────
RECOMMENDATIONS = {
    'Plastik': {
        'icon': '♻️', 'color': '#06b6d4',
        'tips': [
            'Pisahkan ke tempat sampah daur ulang plastik (biasanya berwarna kuning).',
            'Cuci dan keringkan sebelum dibuang agar tidak terkontaminasi.',
            'Jangan campur dengan sampah organik atau B3.',
            'Botol plastik PET (kode 1) bernilai tinggi di bank sampah.',
        ],
        'action': 'Daur Ulang'
    },
    'Kertas': {
        'icon': '📄', 'color': '#f59e0b',
        'tips': [
            'Kumpulkan dan ikat kertas bekas, lalu setor ke bank sampah.',
            'Hindari membasahi kertas sebelum dibuang agar tetap bernilai.',
            'Kardus bisa dilipat agar hemat tempat.',
            'Kertas yang sudah terkena minyak/makanan sebaiknya dikomposkan.',
        ],
        'action': 'Daur Ulang / Kompos'
    },
    'Kaca': {
        'icon': '🪟', 'color': '#8b5cf6',
        'tips': [
            'Bungkus pecahan kaca dengan kertas tebal sebelum dibuang.',
            'Pisahkan ke tempat sampah anorganik.',
            'Botol kaca utuh bisa disetor ke pengepul atau bank sampah.',
            'Jangan bakar kaca — berbahaya dan menghasilkan gas beracun.',
        ],
        'action': 'Pisahkan Khusus'
    },
    'Logam': {
        'icon': '⚙️', 'color': '#10d9a0',
        'tips': [
            'Setor ke pengepul logam — kaleng aluminium, besi, dan tembaga bernilai tinggi.',
            'Bersihkan dari sisa makanan/minyak sebelum disetor.',
            'Jangan buang ke tempat sampah biasa karena sulit terurai.',
            'Aerosol kosong bisa dibuang ke tempat sampah B3.',
        ],
        'action': 'Jual ke Pengepul'
    },
    'Organik': {
        'icon': '🌿', 'color': '#4ade80',
        'tips': [
            'Jadikan kompos dengan mencampurnya dengan daun kering atau tanah.',
            'Sisa makanan bisa diolah menjadi pupuk cair fermentasi (eco-enzyme).',
            'Pisahkan dari sampah anorganik agar tidak mencemari daur ulang.',
            'Gunakan komposter atau lubang resapan biopori di rumah.',
        ],
        'action': 'Kompos'
    },
}

# ─── Konfigurasi Realtime YOLO ─────────────────────────────────────────────────
YOLO_CONF = 0.40   # threshold lebih rendah, dikompensasi temporal smoothing
YOLO_IOU  = 0.45

# ─── Temporal Smoothing & Anti-Flicker ─────────────────────────────────────────
SMOOTH_WINDOW = 5   # jumlah frame untuk majority voting & confidence averaging
HOLD_FRAMES   = 4   # toleransi objek "hilang" sebelum benar-benar dihapus dari layar

track_history = defaultdict(lambda: {
    'labels': deque(maxlen=SMOOTH_WINDOW),
    'confs':  deque(maxlen=SMOOTH_WINDOW),
    'bbox':   None,
    'misses': 0,
})

# Lock agar inference + update track_history tidak overlap antar request
inference_lock = threading.Lock()

# ─── Load Model ───────────────────────────────────────────────────────────────
model_yolo  = None
model_keras = None
yolo_path_used = None

def load_models():
    global model_yolo, model_keras, yolo_path_used

    # Load YOLOv8
    for yolo_path in YOLO_CANDIDATES:
        if os.path.exists(yolo_path):
            try:
                from ultralytics import YOLO
                model_yolo = YOLO(yolo_path)
                model_yolo.to('cpu')
                yolo_path_used = yolo_path
                print(f"[✓] YOLOv8 model loaded: {yolo_path}")
                break
            except Exception as e:
                print(f"[✗] YOLOv8 load error ({yolo_path}): {e}")

    if not model_yolo:
        print("[!] YOLOv8 model tidak ditemukan — camera akan pakai demo mode")

    # Load Keras model
    if os.path.exists(MODEL_PATH_KERAS):
        try:
            import tensorflow as tf
            model_keras = tf.keras.models.load_model(MODEL_PATH_KERAS)
            print(f"[✓] Keras model loaded: {MODEL_PATH_KERAS}")
        except Exception as e:
            print(f"[✗] Keras load error: {e}")
    else:
        print("[!] Keras model tidak ditemukan — klasifikasi akan pakai demo mode")


def preprocess_image(img_array):
    img = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    img = img.astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)


def predict_keras(img_array):
    processed = preprocess_image(img_array)
    predictions = model_keras.predict(processed, verbose=0)[0]
    pred_idx    = int(np.argmax(predictions))
    confidence  = float(predictions[pred_idx])
    all_scores  = {CLASS_NAMES_KERAS[i]: float(predictions[i]) for i in range(len(CLASS_NAMES_KERAS))}
    return CLASS_NAMES_KERAS[pred_idx], confidence, all_scores


def predict_demo(img_array):
    mean_color = img_array.mean(axis=(0, 1))
    r, g, b = mean_color[2], mean_color[1], mean_color[0]
    if r > g and r > b:       label, conf = 'Plastik', 0.873
    elif g > r and g > b:     label, conf = 'Organik', 0.812
    elif b > r and b > g:     label, conf = 'Kaca',    0.756
    elif r > 150 and g > 150: label, conf = 'Kertas',  0.834
    else:                     label, conf = 'Logam',   0.791
    remaining = 1 - conf
    others    = [c for c in CLASS_NAMES_KERAS if c != label]
    scores    = {label: conf}
    splits    = sorted(np.random.dirichlet(np.ones(4)) * remaining, reverse=True)
    for i, c in enumerate(others):
        scores[c] = float(splits[i])
    return label, conf, scores


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html', page='home')

@app.route('/klasifikasi')
def klasifikasi():
    return render_template('klasifikasi.html', page='klasifikasi')

@app.route('/camera')
def camera():
    return render_template('camera.html', page='camera')

@app.route('/about')
def about():
    return render_template('about.html', page='about')


@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'Tidak ada file gambar'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file dipilih'}), 400

    img_bytes = file.read()
    nparr     = np.frombuffer(img_bytes, np.uint8)
    img_bgr   = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img_bgr is None:
        return jsonify({'error': 'Gagal membaca gambar'}), 400

    try:
        if model_keras:
            label, confidence, all_scores = predict_keras(img_bgr)
            model_used = 'MobileNetV2'
        else:
            label, confidence, all_scores = predict_demo(img_bgr)
            model_used = 'Demo Mode'
    except Exception as e:
        return jsonify({'error': f'Prediksi gagal: {str(e)}'}), 500

    rec = RECOMMENDATIONS.get(label, {})
    return jsonify({
        'success':        True,
        'prediction':     label,
        'confidence':     round(confidence * 100, 1),
        'all_scores':     {k: round(v * 100, 1) for k, v in
                           sorted(all_scores.items(), key=lambda x: x[1], reverse=True)},
        'recommendation': rec,
        'model_used':     model_used,
    })


@app.route('/api/camera-frame', methods=['POST'])
def camera_frame():
    data = request.get_json()
    if not data or 'frame' not in data:
        return jsonify({'error': 'No frame data'}), 400

    try:
        frame_data  = data['frame'].split(',')[1]
        frame_bytes = base64.b64decode(frame_data)
        nparr       = np.frombuffer(frame_bytes, np.uint8)
        frame       = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError('cv2.imdecode returned None')
    except Exception as e:
        return jsonify({'error': f'Frame decode error: {str(e)}'}), 400

    # FIX: ambil resolusi frame dari client agar scaling bbox akurat
    send_w = int(data.get('send_w', frame.shape[1]))
    send_h = int(data.get('send_h', frame.shape[0]))

    t_start    = time.time()
    detections = []

    if model_yolo:
        try:
            current_ids = set()

            with inference_lock:
                try:
                    # Tracking aktif → setiap objek punya track_id konsisten antar-frame
                    results = model_yolo.track(
                        frame,
                        conf    = YOLO_CONF,
                        iou     = YOLO_IOU,
                        imgsz   = 640,
                        persist = True,
                        tracker = 'bytetrack.yaml',
                        verbose = False,
                        device  = 'cpu',
                    )
                except Exception:
                    # Fallback jika dependency tracker ('lap'/'lapx') belum terpasang
                    results = model_yolo.predict(
                        frame,
                        conf    = YOLO_CONF,
                        iou     = YOLO_IOU,
                        imgsz   = 640,
                        verbose = False,
                        device  = 'cpu',
                    )

                for result in results:
                    boxes = result.boxes
                    if boxes is None or len(boxes) == 0:
                        continue
                    for box in boxes:
                        cls_id = int(box.cls[0])
                        conf   = float(box.conf[0])
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        x1 = max(0, min(int(x1), send_w))
                        y1 = max(0, min(int(y1), send_h))
                        x2 = max(0, min(int(x2), send_w))
                        y2 = max(0, min(int(y2), send_h))
                        if (x2 - x1) < 20 or (y2 - y1) < 20:
                            continue

                        label    = YOLO_CLASS_MAP.get(cls_id, f'Kelas {cls_id}')
                        track_id = int(box.id[0]) if box.id is not None else None

                        if track_id is None:
                            # Tracker non-aktif (fallback predict) → tampilkan langsung
                            rec = RECOMMENDATIONS.get(label, {})
                            detections.append({
                                'label':      label,
                                'confidence': round(conf * 100, 1),
                                'bbox':       [x1, y1, x2, y2],
                                'color':      rec.get('color', '#10d9a0'),
                                'icon':       rec.get('icon', '♻️'),
                                'action':     rec.get('action', 'Pisahkan'),
                            })
                            continue

                        current_ids.add(track_id)
                        hist = track_history[track_id]
                        hist['labels'].append(label)
                        hist['confs'].append(conf)
                        hist['bbox']   = [x1, y1, x2, y2]
                        hist['misses'] = 0

                # ── Majority voting + confidence averaging + hold-last detection ──
                for tid in list(track_history.keys()):
                    hist = track_history[tid]

                    if tid not in current_ids:
                        hist['misses'] += 1
                        if hist['misses'] > HOLD_FRAMES:
                            del track_history[tid]
                            continue

                    if not hist['labels']:
                        continue

                    stable_label = Counter(hist['labels']).most_common(1)[0][0]
                    avg_conf     = sum(hist['confs']) / len(hist['confs'])
                    rec          = RECOMMENDATIONS.get(stable_label, {})

                    detections.append({
                        'label':      stable_label,
                        'confidence': round(avg_conf * 100, 1),
                        'bbox':       hist['bbox'],
                        'color':      rec.get('color', '#10d9a0'),
                        'icon':       rec.get('icon', '♻️'),
                        'action':     rec.get('action', 'Pisahkan'),
                    })

        except Exception as e:
            return jsonify({'error': f'YOLO error: {str(e)}', 'detections': []}), 200
    else:
        # Demo mode
        h, w = send_h, send_w
        rec  = RECOMMENDATIONS.get('Plastik', {})
        detections.append({
            'label':      'Plastik',
            'confidence': round(85 + np.random.rand() * 10, 1),
            'bbox':       [w//4, h//4, 3*w//4, 3*h//4],
            'color':      rec.get('color', '#06b6d4'),
            'icon':       rec.get('icon', '♻️'),
            'action':     rec.get('action', 'Daur Ulang'),
        })

    inference_ms = round((time.time() - t_start) * 1000)
    return jsonify({
        'success':      True,
        'detections':   detections,
        'inference_ms': inference_ms,
        'model':        'YOLOv8m' if model_yolo else 'Demo',
    })


@app.route('/api/status')
def status():
    return jsonify({
        'keras_model':   model_keras is not None,
        'yolo_model':    model_yolo is not None,
        'yolo_path':     yolo_path_used,
        'classes_keras': CLASS_NAMES_KERAS,
        'classes_yolo':  list(YOLO_CLASS_MAP.values()),
        'demo_mode':     model_keras is None and model_yolo is None,
    })


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    load_models()
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)