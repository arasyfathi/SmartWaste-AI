import os                                                  # akses environment variable & path file
import io                                                  # (tidak dipakai langsung di sini, dipakai modul lain)
import base64                                              # decode frame kamera yang dikirim sebagai base64
import json                                                # serialisasi log riwayat ke riwayat.jsonl
import time                                                # mengukur waktu inferensi (ms)
import threading                                           # lock supaya inference tidak overlap antar request
from collections import deque, defaultdict, Counter        # struktur data untuk smoothing & voting deteksi
import numpy as np                                         # operasi array gambar/angka
from flask import Flask, render_template, request, jsonify, Response  # framework web & helper response
from PIL import Image                                      # (tidak dipakai langsung, cadangan utilitas gambar)
import cv2                                                  # decode/resize/convert gambar (OpenCV)
import uuid                                                 # generate nama file unik saat upload ke Drive
from datetime import datetime                               # timestamp untuk nama file & log riwayat
from drive_storage import upload_to_drive_async              # upload hasil prediksi ke Google Drive di background

app = Flask(__name__)                                       # inisialisasi aplikasi Flask
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max upload  # batas ukuran body request (anti DoS upload besar)

# ─── Validasi file upload (server-side) ────────────────────────────────────────
# Sebelumnya validasi tipe/ukuran file HANYA ada di klasifikasi.js (client-side),
# sehingga gampang dilewati dengan request langsung (curl/Postman) ke /api/predict.
# Sekarang divalidasi juga di server: ekstensi + MIME type yang dikirim browser.
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}      # ekstensi file gambar yang diizinkan
ALLOWED_MIME_TYPES  = {'image/jpeg', 'image/png', 'image/webp'}  # MIME type yang diizinkan

# ─── Deteksi GPU otomatis ──────────────────────────────────────────────────────
# Sebelumnya CUDA_VISIBLE_DEVICES di-set '' di sini sehingga GPU selalu dimatikan
# dan semua inference YOLO jatuh ke CPU (penyebab utama frame lag & inferensi
# 4-17 detik/frame). Sekarang device dipilih otomatis: pakai GPU jika tersedia,
# fallback ke CPU jika tidak ada.
try:
    import torch  # type: ignore                              # cek ketersediaan PyTorch/CUDA
    YOLO_DEVICE = 0 if torch.cuda.is_available() else 'cpu'  # device index 0 (GPU) atau 'cpu'
    YOLO_HALF   = torch.cuda.is_available()  # FP16 di GPU → lebih cepat lagi  # half-precision hanya valid di GPU
    if torch.cuda.is_available():
        print(f"[OK] GPU terdeteksi: {torch.cuda.get_device_name(0)} - YOLO akan pakai GPU")  # log nama GPU
    else:
        print("[!] GPU tidak terdeteksi - YOLO fallback ke CPU (akan lebih lambat)")  # log fallback CPU
except ImportError:
    YOLO_DEVICE = 'cpu'                                      # torch tidak terpasang → paksa CPU
    YOLO_HALF   = False                                       # FP16 tidak relevan di CPU
    print("[!] PyTorch tidak ditemukan - fallback ke CPU")    # log peringatan dependency hilang

# ─── Konfigurasi ──────────────────────────────────────────────────────────────
MODEL_PATH_KERAS    = 'model/classification/smartwaste_mobilenetv2.keras'  # path model MobileNetV2
IMG_SIZE            = 224                                       # ukuran input gambar untuk MobileNetV2 (224x224)
CONFIDENCE_THRESHOLD = 0.60  # threshold minimum confidence MobileNetV2:
                              # jika confidence tertinggi < 60%, prediksi dianggap "Tidak Dikenali"

# Path YOLO: cek hasil training baru dulu, fallback ke model lama
YOLO_CANDIDATES = [
    'model/yolo/smartwaste_yolo.pt',                         # lokasi model YOLO hasil training terbaru
    'model/smartwaste_yolo.pt'                               # fallback lokasi lama
]
MODEL_PATH_YOLO = next((p for p in YOLO_CANDIDATES if os.path.exists(p)), None)  # pilih path pertama yang ada

# Kelas Keras (5 kelas Indonesia)
CLASS_NAMES_KERAS = ['Kaca', 'Kertas', 'Logam', 'Organik', 'Plastik']  # urutan harus sama dengan saat training

# Kelas YOLO (5 kelas, hasil remap dataset Roboflow 6→5) → mapping ke nama Indonesia
# Urutan sesuai data.yaml hasil remap: kaca, kertas, logam, organik, plastik (alfabetis)
YOLO_CLASS_MAP = {
    0: 'Kaca',                                               # index class_id 0 dari model YOLO → label "Kaca"
    1: 'Kertas',
    2: 'Logam',
    3: 'Organik',
    4: 'Plastik',
}

# ─── Rekomendasi per kategori ─────────────────────────────────────────────────
RECOMMENDATIONS = {                                          # data statis: ikon, warna, dan tips penanganan per kategori
    'Plastik': {
        'icon': '♻️', 'color': '#06b6d4',                    # emoji & warna badge ditampilkan di UI
        'tips': [
            'Pisahkan ke tempat sampah daur ulang plastik (biasanya berwarna kuning).',
            'Cuci dan keringkan sebelum dibuang agar tidak terkontaminasi.',
            'Jangan campur dengan sampah organik atau B3.',
            'Botol plastik PET (kode 1) bernilai tinggi di bank sampah.',
        ],
        'action': 'Daur Ulang'                               # label aksi singkat ditampilkan ke user
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
YOLO_CONF = 0.60   # threshold tinggi: hanya tampilkan deteksi yang model benar-benar yakin
YOLO_IOU  = 0.45  # NMS YOLO standar — duplikasi same-class dihapus YOLO sendiri
# imgsz khusus untuk live camera dikecilkan dari 640 → 480 (training tetap 640).
# Mengurangi resolusi input mempercepat inference secara signifikan, terutama
# penting kalau device akhirnya tetap fallback ke CPU.
YOLO_IMGSZ_CAMERA = 416                                      # resolusi input inference untuk frame kamera

# ─── Temporal Smoothing & Anti-Flicker ─────────────────────────────────────────
SMOOTH_WINDOW = 5   # butuh 5 frame konsisten → kurangi flicker & false positive sesaat
HOLD_FRAMES   = 1   # objek yang hilang hanya ditahan 1 frame sebelum dihapus
MIN_CONF_DISPLAY = 0.62  # threshold minimum avg confidence untuk ditampilkan ke user

track_history = defaultdict(lambda: {                        # riwayat per track_id objek yang terdeteksi kamera
    'labels': deque(maxlen=SMOOTH_WINDOW),                    # antrian label terbaru (maks 5) untuk voting
    'confs':  deque(maxlen=SMOOTH_WINDOW),                    # antrian confidence terbaru (maks 5)
    'bbox':   None,                                           # bounding box terakhir yang diketahui
    'misses': 0,                                               # jumlah frame berturut-turut objek tidak terdeteksi
})

# Lock agar inference + update track_history tidak overlap antar request
inference_lock = threading.Lock()                            # mutex supaya 2 request kamera tidak race condition

# ─── Load Model ───────────────────────────────────────────────────────────────
model_yolo  = None                                            # placeholder model YOLO sebelum di-load
model_keras = None                                            # placeholder model Keras sebelum di-load
yolo_path_used = None                                         # mencatat path YOLO mana yang berhasil dimuat

def load_models():
    global model_yolo, model_keras, yolo_path_used            # ubah variabel global, bukan lokal

    # Load YOLOv8
    for yolo_path in YOLO_CANDIDATES:                          # coba tiap kandidat path YOLO secara berurutan
        if os.path.exists(yolo_path):                          # hanya proses jika file benar-benar ada
            try:
                from ultralytics import YOLO  # type: ignore  # import lazy supaya start lebih cepat jika tak dipakai
                model_yolo = YOLO(yolo_path)                   # load bobot model YOLO dari file .pt
                model_yolo.to(YOLO_DEVICE)                      # pindahkan model ke GPU/CPU sesuai deteksi device
                yolo_path_used = yolo_path                      # simpan path yang berhasil dipakai
                print(f"[OK] YOLOv8 model loaded: {yolo_path} (device={YOLO_DEVICE})")
                break                                            # berhenti setelah satu model berhasil dimuat
            except Exception as e:
                print(f"[X] YOLOv8 load error ({yolo_path}): {e}")  # log error, lanjut coba kandidat berikutnya

    if not model_yolo:
        print("[!] YOLOv8 model tidak ditemukan - camera akan pakai demo mode")  # info jika semua kandidat gagal

    # Load Keras model
    if os.path.exists(MODEL_PATH_KERAS):                       # cek file model klasifikasi ada
        try:
            import tensorflow as tf                            # import lazy TensorFlow
            model_keras = tf.keras.models.load_model(MODEL_PATH_KERAS)  # load model MobileNetV2 (.keras)
            print(f"[OK] Keras model loaded: {MODEL_PATH_KERAS}")
        except Exception as e:
            print(f"[X] Keras load error: {e}")                 # log error tanpa menghentikan server
    else:
        print("[!] Keras model tidak ditemukan - klasifikasi akan pakai demo mode")


def preprocess_image(img_array):
    # FIX: model Keras (MobileNetV2) dilatih dengan ImageDataGenerator/PIL yang
    # membaca gambar sebagai RGB. img_array di sini datang dari cv2.imdecode()
    # yang formatnya BGR — kalau tidak dikonversi, kanal merah & biru tertukar
    # saat inference (mismatch dengan training), bisa menurunkan akurasi
    # prediksi secara diam-diam tanpa error apa pun.
    img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)           # konversi BGR (OpenCV) → RGB (sesuai training)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))                # resize ke 224x224 sesuai input MobileNetV2
    img = img.astype(np.float32) / 255.0                       # normalisasi pixel ke rentang 0–1
    return np.expand_dims(img, axis=0)                         # tambah dimensi batch → shape (1, 224, 224, 3)


def predict_keras(img_array):
    processed = preprocess_image(img_array)                    # preprocessing gambar sebelum masuk model
    predictions = model_keras.predict(processed, verbose=0)[0]  # jalankan inference, ambil hasil batch ke-0
    pred_idx    = int(np.argmax(predictions))                   # index kelas dengan probabilitas tertinggi
    confidence  = float(predictions[pred_idx])                  # nilai confidence kelas terpilih
    all_scores  = {CLASS_NAMES_KERAS[i]: float(predictions[i]) for i in range(len(CLASS_NAMES_KERAS))}  # skor semua kelas
    return CLASS_NAMES_KERAS[pred_idx], confidence, all_scores  # label, confidence, dan semua skor


def allowed_file(filename, mimetype):
    ext_ok  = os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS  # cek ekstensi file valid
    mime_ok = mimetype in ALLOWED_MIME_TYPES                    # cek MIME type valid
    return ext_ok and mime_ok                                   # file diterima hanya jika keduanya valid


def warmup_models():
    """
    Inferensi pertama setelah model di-load ke GPU biasanya jauh lebih lambat
    (cuDNN/cuda melakukan auto-tuning kernel saat pertama dipanggil). Tanpa
    warmup, USER PERTAMA yang membuka kamera akan kena delay belasan detik itu.
    Warmup di sini "membakar" delay tersebut saat server baru start, bukan
    saat user sedang menunggu.
    """
    dummy = np.zeros((480, 640, 3), dtype=np.uint8)             # gambar hitam dummy untuk pemanasan model

    if model_yolo:
        try:
            t0 = time.time()                                     # catat waktu mulai warmup
            model_yolo.predict(dummy, imgsz=YOLO_IMGSZ_CAMERA, device=YOLO_DEVICE,
                                half=YOLO_HALF, verbose=False)    # jalankan satu inference dummy
            print(f"[OK] YOLOv8 warmup selesai ({round((time.time()-t0)*1000)}ms)")
        except Exception as e:
            print(f"[!] YOLOv8 warmup gagal (diabaikan): {e}")    # warmup gagal tidak fatal, lanjut start server

    if model_keras:
        try:
            t0 = time.time()                                     # catat waktu mulai warmup Keras
            predict_keras(dummy)                                  # jalankan satu inference dummy
            print(f"[OK] Keras warmup selesai ({round((time.time()-t0)*1000)}ms)")
        except Exception as e:
            print(f"[!] Keras warmup gagal (diabaikan): {e}")




# ─── Manual cross-class NMS helper ────────────────────────────────────────────
def _nms_detections(raw_boxes, iou_thresh=0.45, frame_w=640, frame_h=360):
    """
    NMS lintas kelas dengan dua metrik overlap:
      1. IoU standar      — untuk objek seukuran
      2. IoMin (overlap/min_area) — untuk bbox kecil di dalam bbox besar
         (misal tutup botol di dalam badan botol)
    Juga memfilter:
      - bbox yang area-nya > 80% frame (background/noise)
      - bbox yang area-nya < 0.5% frame (terlalu kecil, bukan objek nyata)
    """
    if not raw_boxes:
        return raw_boxes                                        # tidak ada box → langsung kembalikan list kosong

    frame_area = frame_w * frame_h                               # luas total frame, dipakai untuk filter rasio area
    filtered = []
    for b in raw_boxes:
        bx1, by1, bx2, by2 = b[4], b[5], b[6], b[7]              # koordinat bbox dari tuple deteksi
        area = (bx2 - bx1) * (by2 - by1)                          # hitung luas bbox
        if area <= 0:
            continue                                              # buang bbox tidak valid (area nol/negatif)
        ratio = area / frame_area                                 # rasio luas bbox terhadap frame
        # Hapus bbox yang terlalu kecil (< 0.5% frame) atau terlalu besar (> 80% frame)
        if ratio < 0.005 or ratio > 0.80:
            continue                                              # buang noise kecil atau bbox sebesar background
        filtered.append(b)                                        # bbox valid, masuk daftar kandidat NMS

    if len(filtered) <= 1:
        return filtered                                           # 0 atau 1 box tidak perlu NMS

    # Sort by conf descending
    filtered = sorted(filtered, key=lambda b: b[0], reverse=True)  # urutkan: confidence tertinggi diproses dulu
    keep = []                                                      # daftar box yang lolos (final)
    suppressed = set()                                             # index box yang sudah ditekan/dihapus
    for i, b in enumerate(filtered):
        if i in suppressed:
            continue                                               # box ini sudah ditekan, skip
        keep.append(b)                                             # box dengan conf tertinggi yang belum ditekan → simpan
        bx1, by1, bx2, by2 = b[4], b[5], b[6], b[7]
        area_b = (bx2-bx1)*(by2-by1)                                # luas box acuan saat ini
        for j, b2 in enumerate(filtered[i+1:], i+1):
            if j in suppressed:
                continue                                            # box pembanding sudah ditekan, skip
            ax1, ay1, ax2, ay2 = b2[4], b2[5], b2[6], b2[7]
            area_b2 = (ax2-ax1)*(ay2-ay1)                            # luas box pembanding
            ix1 = max(bx1, ax1); iy1 = max(by1, ay1)                 # koordinat kiri-atas area overlap
            ix2 = min(bx2, ax2); iy2 = min(by2, ay2)                 # koordinat kanan-bawah area overlap
            iw = max(0, ix2 - ix1); ih = max(0, iy2 - iy1)            # lebar & tinggi overlap (0 jika tak overlap)
            inter = iw * ih                                          # luas area overlap (intersection)
            union = area_b + area_b2 - inter                         # luas gabungan dua box (union)
            # IoU standar
            iou = inter / union if union > 0 else 0                  # rasio intersection/union
            # IoMin: overlap dibagi area yang lebih kecil (deteksi bbox kecil di dalam bbox besar)
            iomin = inter / min(area_b, area_b2) if min(area_b, area_b2) > 0 else 0  # rasio overlap thd box terkecil
            if iou > iou_thresh or iomin > 0.75:
                suppressed.add(j)                                    # box dianggap duplikat → ditekan/dihapus
    return keep                                                      # hasil akhir box setelah NMS

# ─── Error Handlers ───────────────────────────────────────────────────────────
@app.errorhandler(413)
def file_too_large(e):
    return jsonify({'error': 'Ukuran file terlalu besar (maksimal 10MB).'}), 413  # respons saat upload > MAX_CONTENT_LENGTH


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint tidak ditemukan'}), 404         # respons JSON untuk route yang tidak ada


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Terjadi kesalahan internal pada server'}), 500  # respons JSON untuk error tak terduga


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html', page='home')          # render halaman Home

@app.route('/klasifikasi')
def klasifikasi():
    return render_template('klasifikasi.html', page='klasifikasi')  # render halaman upload & klasifikasi gambar

@app.route('/camera')
def camera():
    return render_template('camera.html', page='camera')        # render halaman deteksi kamera real-time

@app.route('/about')
def about():
    return render_template('about.html', page='about')          # render halaman informasi proyek


@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'Tidak ada file gambar'}), 400  # request tidak menyertakan field 'image'

    file = request.files['image']                                # ambil file upload dari form-data
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file dipilih'}), 400  # field ada tapi nama file kosong

    if not allowed_file(file.filename, file.mimetype):
        return jsonify({'error': 'Format file tidak didukung. Gunakan JPG, PNG, atau WEBP.'}), 400  # validasi tipe file

    img_bytes = file.read()                                       # baca seluruh isi file sebagai bytes
    nparr     = np.frombuffer(img_bytes, np.uint8)                 # ubah bytes jadi array uint8
    img_bgr   = cv2.imdecode(nparr, cv2.IMREAD_COLOR)              # decode array jadi gambar OpenCV (BGR)

    if img_bgr is None:
        return jsonify({'error': 'Gagal membaca gambar'}), 400     # file bukan gambar valid / corrupt

    if not model_keras:
        return jsonify({'error': 'Model klasifikasi tidak tersedia. Pastikan file model sudah ada di model/classification/.'}), 503  # model belum dimuat

    try:
        label, confidence, all_scores = predict_keras(img_bgr)     # jalankan klasifikasi MobileNetV2
        model_used = 'MobileNetV2'                                  # label model yang dipakai, untuk response
    except Exception as e:
        return jsonify({'error': f'Prediksi gagal: {str(e)}'}), 500  # tangani error saat inference

    # ─── Confidence threshold — tolak prediksi yang tidak meyakinkan ──────
    # Jika skor tertinggi model < CONFIDENCE_THRESHOLD (60%), gambar yang
    # diupload kemungkinan bukan sampah yang dikenal model. Daripada memaksa
    # ke salah satu kelas, label diubah ke "Tidak Dikenali" dan rekomendasi
    # dikosongkan agar frontend tidak menampilkan tips yang menyesatkan.
    if confidence < CONFIDENCE_THRESHOLD:
        label = 'Tidak Dikenali'
        rec   = {
            'icon':   '❓',
            'color':  '#6b7280',                                     # warna netral abu-abu
            'tips':   ['Tolong unggah gambar sampah yang lebih jelas.'],
            'action': 'Tidak Dikenali',
        }
    else:
        rec = RECOMMENDATIONS.get(label, {})                         # ambil data rekomendasi sesuai label prediksi

    # ─── Upload ke Google Drive (background, tidak menunda response) ──────
    ext = os.path.splitext(file.filename)[1].lower()               # ambil ekstensi file asli
    drive_filename = f"{datetime.now():%Y%m%d_%H%M%S}_{uuid.uuid4().hex[:8]}{ext}"  # nama file unik berbasis waktu+uuid

    def _log_drive_upload(file_id, link):
        if file_id:                                                  # hanya log jika upload Drive berhasil
            entry = {
                'filename':   drive_filename,
                'drive_file_id': file_id,
                'drive_link': link,
                'prediction': label,                                  # label sudah di-override jika di bawah threshold
                'confidence': round(confidence * 100, 1),
                'timestamp':  datetime.now().isoformat(),
            }
            with open('riwayat.jsonl', 'a') as f:                    # append entry sebagai satu baris JSON
                f.write(json.dumps(entry) + '\n')

    upload_to_drive_async(img_bytes, drive_filename, file.mimetype, on_done=_log_drive_upload)  # upload async, callback saat selesai

    return jsonify({
        'success':        True,
        'prediction':     label,                                     # kelas hasil prediksi (atau "Tidak Dikenali")
        'confidence':     round(confidence * 100, 1),                 # confidence model mentah dalam persen
        'all_scores':     {k: round(v * 100, 1) for k, v in
                           sorted(all_scores.items(), key=lambda x: x[1], reverse=True)},  # semua skor, diurutkan desc
        'recommendation': rec,                                        # ikon, warna, tips, dan aksi (kosong jika tidak dikenali)
        'model_used':     model_used,                                 # info model yang dipakai
    })

@app.route('/api/camera-frame', methods=['POST'])
def camera_frame():
    data = request.get_json()                                        # ambil body JSON dari request
    if not data or 'frame' not in data:
        return jsonify({'error': 'No frame data'}), 400                # body tidak valid / field frame tidak ada

    try:
        frame_data  = data['frame'].split(',')[1]                      # buang prefix "data:image/...;base64,"
        frame_bytes = base64.b64decode(frame_data)                     # decode base64 → bytes gambar
        nparr       = np.frombuffer(frame_bytes, np.uint8)              # bytes → array uint8
        frame       = cv2.imdecode(nparr, cv2.IMREAD_COLOR)             # decode array → gambar OpenCV (BGR)
        if frame is None:
            raise ValueError('cv2.imdecode returned None')              # gambar gagal didecode
    except Exception as e:
        return jsonify({'error': f'Frame decode error: {str(e)}'}), 400  # tangani semua error decoding frame

    # FIX: ambil resolusi frame dari client agar scaling bbox akurat
    send_w = int(data.get('send_w', frame.shape[1]))                    # lebar frame asli dari sisi client
    send_h = int(data.get('send_h', frame.shape[0]))                    # tinggi frame asli dari sisi client

    t_start    = time.time()                                            # mulai hitung waktu inferensi
    detections = []                                                      # list hasil deteksi yang akan dikirim ke client

    if model_yolo:
        try:
            current_ids = set()                                          # track_id yang muncul di frame ini

            with inference_lock:                                         # cegah race condition antar request paralel
                try:
                    # Tracking aktif → setiap objek punya track_id konsisten antar-frame
                    results = model_yolo.track(
                        frame,
                        conf    = YOLO_CONF,                              # ambang minimum confidence deteksi
                        iou     = YOLO_IOU,                                # ambang IoU untuk NMS internal YOLO
                        imgsz   = YOLO_IMGSZ_CAMERA,                       # resolusi input inference
                        persist = True,                                    # pertahankan track_id antar frame
                        tracker = 'bytetrack.yaml',                        # algoritma tracking yang dipakai
                        verbose = False,                                    # nonaktifkan log bawaan ultralytics
                        device  = YOLO_DEVICE,                              # device inference (GPU/CPU)
                        half    = YOLO_HALF,                                # gunakan FP16 jika di GPU
                        max_det = 5,                                        # batas maksimal objek per frame
                    )
                except Exception:
                    # Fallback jika dependency tracker ('lap'/'lapx') belum terpasang
                    results = model_yolo.predict(
                        frame,
                        conf    = YOLO_CONF,
                        iou     = YOLO_IOU,
                        imgsz   = YOLO_IMGSZ_CAMERA,
                        verbose = False,
                        device  = YOLO_DEVICE,
                        half    = YOLO_HALF,
                        max_det = 5,
                    )                                                       # mode tanpa tracking (tanpa track_id)

                # Kumpulkan raw boxes dulu, lalu NMS lintas kelas
                raw_boxes = []                                              # penampung semua bbox mentah hasil model
                for result in results:
                    boxes = result.boxes                                    # objek bbox hasil dari satu frame
                    if boxes is None or len(boxes) == 0:
                        continue                                            # tidak ada objek terdeteksi, lanjut
                    for box in boxes:
                        cls_id = int(box.cls[0])                             # id kelas hasil deteksi
                        conf   = float(box.conf[0])                          # confidence deteksi
                        x1, y1, x2, y2 = box.xyxy[0].tolist()                # koordinat bbox (format xyxy)
                        x1 = max(0, min(int(x1), send_w))                    # clamp koordinat agar tidak keluar frame
                        y1 = max(0, min(int(y1), send_h))
                        x2 = max(0, min(int(x2), send_w))
                        y2 = max(0, min(int(y2), send_h))
                        if (x2 - x1) < 20 or (y2 - y1) < 20:
                            continue                                        # buang bbox terlalu kecil (noise)
                        label    = YOLO_CLASS_MAP.get(cls_id, f'Kelas {cls_id}')  # mapping id kelas → nama Indonesia
                        track_id = int(box.id[0]) if box.id is not None else None  # ambil track_id jika tracking aktif
                        raw_boxes.append((conf, cls_id, label, track_id, x1, y1, x2, y2))  # simpan sebagai tuple

                # NMS lintas kelas dengan area filter dan IoMin
                raw_boxes = _nms_detections(raw_boxes, iou_thresh=0.45, frame_w=send_w, frame_h=send_h)  # bersihkan duplikat antar kelas

                for (conf, cls_id, label, track_id, x1, y1, x2, y2) in raw_boxes:
                        if track_id is None:
                            # Tracker non-aktif (fallback predict) → filter conf lalu tampilkan
                            if conf < MIN_CONF_DISPLAY:
                                continue                                    # confidence terlalu rendah, jangan tampilkan
                            rec = RECOMMENDATIONS.get(label, {})            # ambil data rekomendasi sesuai label
                            detections.append({
                                'label':      label,
                                'confidence': round(conf * 100, 1),
                                'bbox':       [x1, y1, x2, y2],
                                'color':      rec.get('color', '#10d9a0'),
                                'icon':       rec.get('icon', '♻️'),
                                'action':     rec.get('action', 'Pisahkan'),
                            })
                            continue                                        # lanjut ke box berikutnya

                        current_ids.add(track_id)                           # tandai track_id ini aktif di frame ini
                        hist = track_history[track_id]                       # ambil/buat riwayat untuk track_id ini
                        hist['labels'].append(label)                         # simpan label terbaru ke antrian
                        hist['confs'].append(conf)                           # simpan confidence terbaru ke antrian
                        hist['bbox']   = [x1, y1, x2, y2]                     # update posisi bbox terakhir
                        hist['misses'] = 0                                    # reset hitungan frame hilang

                # ── Majority voting + confidence averaging + hold-last detection ──
                for tid in list(track_history.keys()):                       # iterasi semua track_id yang pernah tercatat
                    hist = track_history[tid]

                    if tid not in current_ids:
                        hist['misses'] += 1                                  # objek tidak terdeteksi di frame ini
                        if hist['misses'] > HOLD_FRAMES:
                            del track_history[tid]                            # sudah lewat batas toleransi → hapus riwayat
                            continue
                        continue                                              # masih dalam toleransi, tetap tunggu frame berikut

                    if not hist['labels']:
                        continue                                              # belum ada data label tersimpan, skip

                    # Weighted voting: setiap label diboboti dengan confidence-nya
                    # → label dengan conf tinggi lebih dominan meskipun jumlah frame sama
                    weighted_scores = defaultdict(float)                      # akumulator skor tiap label
                    for lbl, cf in zip(hist['labels'], hist['confs']):
                        weighted_scores[lbl] += cf                            # tambahkan confidence ke skor labelnya
                    stable_label = max(weighted_scores, key=weighted_scores.get)  # label dengan skor tertinggi
                    avg_conf     = sum(hist['confs']) / len(hist['confs'])     # rata-rata confidence beberapa frame terakhir

                    # Jangan tampilkan jika confidence rata-rata terlalu rendah
                    if avg_conf < MIN_CONF_DISPLAY:
                        continue                                              # confidence rata-rata di bawah threshold, skip

                    rec = RECOMMENDATIONS.get(stable_label, {})               # ambil rekomendasi sesuai label stabil
                    detections.append({
                        'label':      stable_label,
                        'confidence': round(avg_conf * 100, 1),
                        'bbox':       hist['bbox'],
                        'color':      rec.get('color', '#10d9a0'),
                        'icon':       rec.get('icon', '♻️'),
                        'action':     rec.get('action', 'Pisahkan'),
                    })

        except Exception as e:
            return jsonify({'error': f'YOLO error: {str(e)}', 'detections': []}), 200  # error inference, tetap balas 200 agar client tidak crash
    else:
        return jsonify({'error': 'Model deteksi tidak tersedia. Pastikan file model sudah ada di model/yolo/.'}), 503  # model YOLO belum dimuat

    inference_ms = round((time.time() - t_start) * 1000)                    # total waktu proses frame ini (ms)
    device_label = 'GPU' if (isinstance(YOLO_DEVICE, int) or str(YOLO_DEVICE).startswith('cuda')) else 'CPU'  # label device untuk ditampilkan
    return jsonify({
        'success':      True,
        'detections':   detections,                                          # daftar objek terdeteksi
        'inference_ms': inference_ms,                                        # waktu inferensi
        'model':        f'YOLOv8m ({device_label})',                          # info model & device yang dipakai
    })


@app.route('/api/status')
def status():
    device_label = 'GPU' if (isinstance(YOLO_DEVICE, int) or str(YOLO_DEVICE).startswith('cuda')) else 'CPU'  # device aktif saat ini
    return jsonify({
        'keras_model':   model_keras is not None,                            # status model Keras sudah dimuat atau belum
        'yolo_model':    model_yolo is not None,                              # status model YOLO sudah dimuat atau belum
        'yolo_path':     yolo_path_used,                                      # path file YOLO yang dipakai
        'yolo_device':   device_label,                                        # device yang dipakai YOLO
        'classes_keras': CLASS_NAMES_KERAS,                                   # daftar kelas Keras
        'classes_yolo':  list(YOLO_CLASS_MAP.values()),                       # daftar kelas YOLO
        'keras_loaded':  model_keras is not None,                             # duplikat info (kompatibilitas frontend lama)
        'yolo_loaded':   model_yolo is not None,                              # duplikat info (kompatibilitas frontend lama)
    })


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    load_models()                                                            # muat semua model AI sebelum server jalan
    warmup_models()                                                          # lakukan inference dummy agar request pertama tidak lambat

    # DEBUG_MODE dikontrol lewat environment variable, default OFF.
    # PENTING: debug=True mengaktifkan Werkzeug debugger interaktif yang bisa
    # dieksploitasi untuk remote code execution kalau server ini diakses dari
    # luar jaringan lokal (mis. lewat ngrok atau deploy ke cloud). Jangan
    # pernah nyalakan DEBUG_MODE=1 kalau host bisa diakses publik.
    #   Windows  : set DEBUG_MODE=1 && python app.py
    #   Linux/Mac: DEBUG_MODE=1 python app.py
    DEBUG_MODE = os.environ.get('DEBUG_MODE', '0') == '1'                     # baca flag debug dari environment

    # use_reloader=False supaya load_models()/warmup_models() tidak terpanggil
    # dua kali (sebelumnya proses parent+child Werkzeug reloader masing-masing
    # memuat model, kontributor lonjakan delay di awal start).
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=5000, threaded=True, use_reloader=False)  # jalankan server Flask