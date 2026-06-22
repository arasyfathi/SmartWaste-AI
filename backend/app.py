import os
import io
import base64
import json
import time
import threading
from collections import deque, defaultdict, Counter
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import cv2
import uuid
from datetime import datetime
from drive_storage import upload_to_drive_async

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React frontend
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max upload

# ─── File validation ─────────────────────────────────────────────────────────
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp'}

# ─── GPU auto-detection ──────────────────────────────────────────────────────
try:
    import torch
    YOLO_DEVICE = 0 if torch.cuda.is_available() else 'cpu'
    YOLO_HALF = torch.cuda.is_available()
    if torch.cuda.is_available():
        print(f"[OK] GPU terdeteksi: {torch.cuda.get_device_name(0)} - YOLO akan pakai GPU")
    else:
        print("[!] GPU tidak terdeteksi - YOLO fallback ke CPU (akan lebih lambat)")
except ImportError:
    YOLO_DEVICE = 'cpu'
    YOLO_HALF = False
    print("[!] PyTorch tidak ditemukan - fallback ke CPU")

# ─── Configuration ───────────────────────────────────────────────────────────
# Model paths relative to backend/ directory (models are in ../model/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, '..', 'model')

MODEL_PATH_KERAS = os.path.join(MODEL_DIR, 'classification', 'smartwaste_mobilenetv2.keras')
IMG_SIZE = 224

YOLO_CANDIDATES = [
    os.path.join(MODEL_DIR, 'yolo', 'smartwaste_yolo.pt'),
    os.path.join(MODEL_DIR, 'smartwaste_yolo.pt'),
]
MODEL_PATH_YOLO = next((p for p in YOLO_CANDIDATES if os.path.exists(p)), None)

CLASS_NAMES_KERAS = ['Kaca', 'Kertas', 'Logam', 'Organik', 'Plastik']

YOLO_CLASS_MAP = {
    0: 'Kaca',
    1: 'Kertas',
    2: 'Logam',
    3: 'Organik',
    4: 'Plastik',
}

# ─── Recommendations ─────────────────────────────────────────────────────────
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

# ─── Realtime YOLO Config ────────────────────────────────────────────────────
YOLO_CONF = 0.60
YOLO_IOU = 0.45
YOLO_IMGSZ_CAMERA = 416

# ─── Temporal Smoothing ──────────────────────────────────────────────────────
SMOOTH_WINDOW = 5
HOLD_FRAMES = 1
MIN_CONF_DISPLAY = 0.62

track_history = defaultdict(lambda: {
    'labels': deque(maxlen=SMOOTH_WINDOW),
    'confs': deque(maxlen=SMOOTH_WINDOW),
    'bbox': None,
    'misses': 0,
})

inference_lock = threading.Lock()

# ─── Models ──────────────────────────────────────────────────────────────────
model_yolo = None
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
                model_yolo.to(YOLO_DEVICE)
                yolo_path_used = yolo_path
                print(f"[OK] YOLOv8 model loaded: {yolo_path} (device={YOLO_DEVICE})")
                break
            except Exception as e:
                print(f"[X] YOLOv8 load error ({yolo_path}): {e}")

    if not model_yolo:
        print("[!] YOLOv8 model tidak ditemukan - camera akan pakai demo mode")

    # Load Keras model
    if os.path.exists(MODEL_PATH_KERAS):
        try:
            import tensorflow as tf
            model_keras = tf.keras.models.load_model(MODEL_PATH_KERAS)
            print(f"[OK] Keras model loaded: {MODEL_PATH_KERAS}")
        except Exception as e:
            print(f"[X] Keras load error: {e}")
    else:
        print("[!] Keras model tidak ditemukan - klasifikasi akan pakai demo mode")


def preprocess_image(img_array):
    img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)


def predict_keras(img_array):
    processed = preprocess_image(img_array)
    predictions = model_keras.predict(processed, verbose=0)[0]
    pred_idx = int(np.argmax(predictions))
    confidence = float(predictions[pred_idx])
    all_scores = {CLASS_NAMES_KERAS[i]: float(predictions[i]) for i in range(len(CLASS_NAMES_KERAS))}
    return CLASS_NAMES_KERAS[pred_idx], confidence, all_scores


def allowed_file(filename, mimetype):
    ext_ok = os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS
    mime_ok = mimetype in ALLOWED_MIME_TYPES
    return ext_ok and mime_ok


def warmup_models():
    dummy = np.zeros((480, 640, 3), dtype=np.uint8)

    if model_yolo:
        try:
            t0 = time.time()
            model_yolo.predict(dummy, imgsz=YOLO_IMGSZ_CAMERA, device=YOLO_DEVICE,
                               half=YOLO_HALF, verbose=False)
            print(f"[OK] YOLOv8 warmup selesai ({round((time.time()-t0)*1000)}ms)")
        except Exception as e:
            print(f"[!] YOLOv8 warmup gagal (diabaikan): {e}")

    if model_keras:
        try:
            t0 = time.time()
            predict_keras(dummy)
            print(f"[OK] Keras warmup selesai ({round((time.time()-t0)*1000)}ms)")
        except Exception as e:
            print(f"[!] Keras warmup gagal (diabaikan): {e}")


# ─── NMS helper ──────────────────────────────────────────────────────────────
def _nms_detections(raw_boxes, iou_thresh=0.45, frame_w=640, frame_h=360):
    if not raw_boxes:
        return raw_boxes

    frame_area = frame_w * frame_h
    filtered = []
    for b in raw_boxes:
        bx1, by1, bx2, by2 = b[4], b[5], b[6], b[7]
        area = (bx2 - bx1) * (by2 - by1)
        if area <= 0:
            continue
        ratio = area / frame_area
        if ratio < 0.005 or ratio > 0.80:
            continue
        filtered.append(b)

    if len(filtered) <= 1:
        return filtered

    filtered = sorted(filtered, key=lambda b: b[0], reverse=True)
    keep = []
    suppressed = set()
    for i, b in enumerate(filtered):
        if i in suppressed:
            continue
        keep.append(b)
        bx1, by1, bx2, by2 = b[4], b[5], b[6], b[7]
        area_b = (bx2-bx1)*(by2-by1)
        for j, b2 in enumerate(filtered[i+1:], i+1):
            if j in suppressed:
                continue
            ax1, ay1, ax2, ay2 = b2[4], b2[5], b2[6], b2[7]
            area_b2 = (ax2-ax1)*(ay2-ay1)
            ix1 = max(bx1, ax1); iy1 = max(by1, ay1)
            ix2 = min(bx2, ax2); iy2 = min(by2, ay2)
            iw = max(0, ix2 - ix1); ih = max(0, iy2 - iy1)
            inter = iw * ih
            union = area_b + area_b2 - inter
            iou = inter / union if union > 0 else 0
            iomin = inter / min(area_b, area_b2) if min(area_b, area_b2) > 0 else 0
            if iou > iou_thresh or iomin > 0.75:
                suppressed.add(j)
    return keep


# ─── Error Handlers ──────────────────────────────────────────────────────────
@app.errorhandler(413)
def file_too_large(e):
    return jsonify({'error': 'Ukuran file terlalu besar (maksimal 10MB).'}), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint tidak ditemukan'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Terjadi kesalahan internal pada server'}), 500


# ─── API Routes ──────────────────────────────────────────────────────────────
@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'Tidak ada file gambar'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file dipilih'}), 400

    if not allowed_file(file.filename, file.mimetype):
        return jsonify({'error': 'Format file tidak didukung. Gunakan JPG, PNG, atau WEBP.'}), 400

    img_bytes = file.read()
    nparr = np.frombuffer(img_bytes, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img_bgr is None:
        return jsonify({'error': 'Gagal membaca gambar'}), 400

    if not model_keras:
        return jsonify({'error': 'Model klasifikasi tidak tersedia.'}), 503

    try:
        label, confidence, all_scores = predict_keras(img_bgr)
    except Exception as e:
        return jsonify({'error': f'Prediksi gagal: {str(e)}'}), 500

    # Upload to Google Drive (background)
    ext = os.path.splitext(file.filename)[1].lower()
    riwayat_path = os.path.join(BASE_DIR, 'riwayat.jsonl')
    drive_filename = f"{datetime.now():%Y%m%d_%H%M%S}_{uuid.uuid4().hex[:8]}{ext}"

    def _log_drive_upload(file_id, link):
        if file_id:
            entry = {
                'filename': drive_filename,
                'drive_file_id': file_id,
                'drive_link': link,
                'prediction': label,
                'confidence': round(confidence * 100, 1),
                'timestamp': datetime.now().isoformat(),
            }
            with open(riwayat_path, 'a') as f:
                f.write(json.dumps(entry) + '\n')

    upload_to_drive_async(img_bytes, drive_filename, file.mimetype, on_done=_log_drive_upload)

    rec = RECOMMENDATIONS.get(label, {})
    return jsonify({
        'success': True,
        'prediction': label,
        'confidence': round(confidence * 100, 1),
        'all_scores': {k: round(v * 100, 1) for k, v in
                       sorted(all_scores.items(), key=lambda x: x[1], reverse=True)},
        'recommendation': rec,
        'model_used': 'MobileNetV2',
    })


@app.route('/api/camera-frame', methods=['POST'])
def camera_frame():
    data = request.get_json()
    if not data or 'frame' not in data:
        return jsonify({'error': 'No frame data'}), 400

    try:
        frame_data = data['frame'].split(',')[1]
        frame_bytes = base64.b64decode(frame_data)
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError('cv2.imdecode returned None')
    except Exception as e:
        return jsonify({'error': f'Frame decode error: {str(e)}'}), 400

    send_w = int(data.get('send_w', frame.shape[1]))
    send_h = int(data.get('send_h', frame.shape[0]))

    t_start = time.time()
    detections = []

    if model_yolo:
        try:
            current_ids = set()

            with inference_lock:
                try:
                    results = model_yolo.track(
                        frame, conf=YOLO_CONF, iou=YOLO_IOU,
                        imgsz=YOLO_IMGSZ_CAMERA, persist=True,
                        tracker='bytetrack.yaml', verbose=False,
                        device=YOLO_DEVICE, half=YOLO_HALF, max_det=5,
                    )
                except Exception:
                    results = model_yolo.predict(
                        frame, conf=YOLO_CONF, iou=YOLO_IOU,
                        imgsz=YOLO_IMGSZ_CAMERA, verbose=False,
                        device=YOLO_DEVICE, half=YOLO_HALF, max_det=5,
                    )

                raw_boxes = []
                for result in results:
                    boxes = result.boxes
                    if boxes is None or len(boxes) == 0:
                        continue
                    for box in boxes:
                        cls_id = int(box.cls[0])
                        conf = float(box.conf[0])
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        x1 = max(0, min(int(x1), send_w))
                        y1 = max(0, min(int(y1), send_h))
                        x2 = max(0, min(int(x2), send_w))
                        y2 = max(0, min(int(y2), send_h))
                        if (x2 - x1) < 20 or (y2 - y1) < 20:
                            continue
                        label = YOLO_CLASS_MAP.get(cls_id, f'Kelas {cls_id}')
                        track_id = int(box.id[0]) if box.id is not None else None
                        raw_boxes.append((conf, cls_id, label, track_id, x1, y1, x2, y2))

                raw_boxes = _nms_detections(raw_boxes, iou_thresh=0.45, frame_w=send_w, frame_h=send_h)

                for (conf, cls_id, label, track_id, x1, y1, x2, y2) in raw_boxes:
                    if track_id is None:
                        if conf < MIN_CONF_DISPLAY:
                            continue
                        rec = RECOMMENDATIONS.get(label, {})
                        detections.append({
                            'label': label,
                            'confidence': round(conf * 100, 1),
                            'bbox': [x1, y1, x2, y2],
                            'color': rec.get('color', '#10d9a0'),
                            'icon': rec.get('icon', '♻️'),
                            'action': rec.get('action', 'Pisahkan'),
                        })
                        continue

                    current_ids.add(track_id)
                    hist = track_history[track_id]
                    hist['labels'].append(label)
                    hist['confs'].append(conf)
                    hist['bbox'] = [x1, y1, x2, y2]
                    hist['misses'] = 0

                for tid in list(track_history.keys()):
                    hist = track_history[tid]
                    if tid not in current_ids:
                        hist['misses'] += 1
                        if hist['misses'] > HOLD_FRAMES:
                            del track_history[tid]
                            continue
                        continue

                    if not hist['labels']:
                        continue

                    weighted_scores = defaultdict(float)
                    for lbl, cf in zip(hist['labels'], hist['confs']):
                        weighted_scores[lbl] += cf
                    stable_label = max(weighted_scores, key=weighted_scores.get)
                    avg_conf = sum(hist['confs']) / len(hist['confs'])

                    if avg_conf < MIN_CONF_DISPLAY:
                        continue

                    rec = RECOMMENDATIONS.get(stable_label, {})
                    detections.append({
                        'label': stable_label,
                        'confidence': round(avg_conf * 100, 1),
                        'bbox': hist['bbox'],
                        'color': rec.get('color', '#10d9a0'),
                        'icon': rec.get('icon', '♻️'),
                        'action': rec.get('action', 'Pisahkan'),
                    })

        except Exception as e:
            return jsonify({'error': f'YOLO error: {str(e)}', 'detections': []}), 200
    else:
        return jsonify({'error': 'Model deteksi tidak tersedia.'}), 503

    inference_ms = round((time.time() - t_start) * 1000)
    device_label = 'GPU' if (isinstance(YOLO_DEVICE, int) or str(YOLO_DEVICE).startswith('cuda')) else 'CPU'
    return jsonify({
        'success': True,
        'detections': detections,
        'inference_ms': inference_ms,
        'model': f'YOLOv8m ({device_label})',
    })


@app.route('/api/status')
def status():
    device_label = 'GPU' if (isinstance(YOLO_DEVICE, int) or str(YOLO_DEVICE).startswith('cuda')) else 'CPU'
    return jsonify({
        'keras_model': model_keras is not None,
        'yolo_model': model_yolo is not None,
        'yolo_path': yolo_path_used,
        'yolo_device': device_label,
        'classes_keras': CLASS_NAMES_KERAS,
        'classes_yolo': list(YOLO_CLASS_MAP.values()),
        'keras_loaded': model_keras is not None,
        'yolo_loaded': model_yolo is not None,
    })


# ─── Health check (for deployment platforms) ─────────────────────────────────
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})


# ─── Run ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    load_models()
    warmup_models()

    DEBUG_MODE = os.environ.get('DEBUG_MODE', '0') == '1'
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=5000, threaded=True, use_reloader=False)
