# akses environment variable & path file
import os
# decode frame kamera yang dikirim sebagai base64
import base64
# serialisasi log riwayat ke riwayat.jsonl
import json
# mengukur waktu inferensi (ms)
import time
# lock supaya inference tidak overlap antar request
import threading
# struktur data untuk smoothing & voting deteksi
from collections import deque, defaultdict, Counter
# operasi array gambar/angka
import numpy as np
# framework web & helper response
from flask import Flask, request, jsonify
# izinkan cross-origin request dari React frontend
from flask_cors import CORS
# decode/resize/convert gambar (OpenCV)
import cv2
# generate nama file unik saat upload ke Cloudinary
# timestamp untuk nama file & log riwayat
from datetime import datetime
# upload hasil prediksi ke Cloudinary di background
from cloudinary_storage import upload_to_cloudinary_async

# inisialisasi aplikasi Flask
app = Flask(__name__)
# Izinkan semua origin agar React frontend (Vite dev server / Vercel)
# bisa mengakses endpoint /api/* tanpa CORS block di browser.
# Untuk production, ganti origins dengan domain frontend yang sebenarnya.
# aktifkan CORS hanya untuk endpoint /api/
CORS(app, resources={r'/api/*': {'origins': '*'}})
# batas ukuran body request 10MB (anti DoS upload besar)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# ─── Validasi file upload (server-side) ────────────────────────────────────────
# Sebelumnya validasi tipe/ukuran file HANYA ada di klasifikasi.js (client-side),
# sehingga gampang dilewati dengan request langsung (curl/Postman) ke /api/predict.
# Sekarang divalidasi juga di server: ekstensi + MIME type yang dikirim browser.
# ekstensi file gambar yang diizinkan
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png',
                      'image/webp'}  # MIME type yang diizinkan

# ─── Deteksi GPU otomatis ──────────────────────────────────────────────────────
# Sebelumnya CUDA_VISIBLE_DEVICES di-set '' di sini sehingga GPU selalu dimatikan
# dan semua inference YOLO jatuh ke CPU (penyebab utama frame lag & inferensi
# 4-17 detik/frame). Sekarang device dipilih otomatis: pakai GPU jika tersedia,
# fallback ke CPU jika tidak ada.
try:
    import torch  # type: ignore                              # cek ketersediaan PyTorch/CUDA
    # device index 0 (GPU) atau 'cpu'
    YOLO_DEVICE = 0 if torch.cuda.is_available() else 'cpu'
    # FP16 di GPU → lebih cepat lagi  # half-precision hanya valid di GPU
    YOLO_HALF = torch.cuda.is_available()
    if torch.cuda.is_available():
        # log nama GPU
        print(
            f"[OK] GPU terdeteksi: {torch.cuda.get_device_name(0)} - YOLO akan pakai GPU")
    else:
        # log fallback CPU
        print("[!] GPU tidak terdeteksi - YOLO fallback ke CPU (akan lebih lambat)")
except ImportError:
    # torch tidak terpasang → paksa CPU
    YOLO_DEVICE = 'cpu'
    # FP16 tidak relevan di CPU
    YOLO_HALF = False
    # log peringatan dependency hilang
    print("[!] PyTorch tidak ditemukan - fallback ke CPU")

# ─── Konfigurasi ──────────────────────────────────────────────────────────────
# Cek lokasi model (mendukung jalan di lokal maupun dalam Docker/HF)
KERAS_CANDIDATES = [
    '../model/classification/smartwaste_mobilenetv2.keras',  # Path jika run lokal dari folder backend/
    'model/classification/smartwaste_mobilenetv2.keras',     # Path jika run di Docker (app.py dan model sejajar di /app)
    './model/classification/smartwaste_mobilenetv2.keras'
]
MODEL_PATH_KERAS = next((p for p in KERAS_CANDIDATES if os.path.exists(p)), None)

# ukuran input gambar untuk MobileNetV2 (224x224)
IMG_SIZE = 224
CONFIDENCE_THRESHOLD = 0.60  # threshold minimum confidence MobileNetV2:
# jika confidence tertinggi < 60%, prediksi dianggap "Tidak Dikenali"

# Path YOLO: cek hasil training baru dulu, fallback ke model lama
YOLO_CANDIDATES = [
    '../model/yolo/smartwaste_yolo.pt',  # Local
    'model/yolo/smartwaste_yolo.pt',     # Docker
    '../model/smartwaste_yolo.pt',       # Local fallback lama
    'model/smartwaste_yolo.pt'           # Docker fallback lama
]
# pilih path pertama yang ada
MODEL_PATH_YOLO = next((p for p in YOLO_CANDIDATES if os.path.exists(p)), None)

# Kelas Keras (5 kelas Indonesia)
CLASS_NAMES_KERAS = ['Kaca', 'Kertas', 'Logam', 'Organik',
                     'Plastik']  # urutan harus sama dengan saat training

# Kelas YOLO (5 kelas, hasil remap dataset Roboflow 6→5) → mapping ke nama Indonesia
# Urutan sesuai data.yaml hasil remap: kaca, kertas, logam, organik, plastik (alfabetis)
YOLO_CLASS_MAP = {
    # index class_id 0 dari model YOLO → label "Kaca"
    0: 'Kaca',
    1: 'Kertas',
    2: 'Logam',
    3: 'Organik',
    4: 'Plastik',
}

# ─── Rekomendasi per kategori ─────────────────────────────────────────────────
RECOMMENDATIONS = {                                          # data statis: ikon, warna, dan tips penanganan per kategori
    'Plastik': {
        # emoji & warna badge ditampilkan di UI
        'icon': '♻️', 'color': '#06b6d4',
        'tips': [
            'Pisahkan ke tempat sampah daur ulang plastik (biasanya berwarna kuning).',
            'Cuci dan keringkan sebelum dibuang agar tidak terkontaminasi.',
            'Jangan campur dengan sampah organik atau B3.',
            'Botol plastik PET (kode 1) bernilai tinggi di bank sampah.',
        ],
        # label aksi singkat ditampilkan ke user
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
YOLO_CONF = 0.60   # threshold tinggi: hanya tampilkan deteksi yang model benar-benar yakin
YOLO_IOU = 0.45  # NMS YOLO standar — duplikasi same-class dihapus YOLO sendiri
# imgsz khusus untuk live camera dikecilkan dari 640 → 480 (training tetap 640).
# Mengurangi resolusi input mempercepat inference secara signifikan, terutama
# penting kalau device akhirnya tetap fallback ke CPU.
# resolusi input inference untuk frame kamera
YOLO_IMGSZ_CAMERA = 416

# ─── Temporal Smoothing & Anti-Flicker ─────────────────────────────────────────
SMOOTH_WINDOW = 5   # butuh 5 frame konsisten → kurangi flicker & false positive sesaat
HOLD_FRAMES = 1   # objek yang hilang hanya ditahan 1 frame sebelum dihapus
MIN_CONF_DISPLAY = 0.62  # threshold minimum avg confidence untuk ditampilkan ke user

track_history = defaultdict(lambda: {                        # riwayat per track_id objek yang terdeteksi kamera
    # antrian label terbaru (maks 5) untuk voting
    'labels': deque(maxlen=SMOOTH_WINDOW),
    # antrian confidence terbaru (maks 5)
    'confs':  deque(maxlen=SMOOTH_WINDOW),
    # bounding box terakhir yang diketahui
    'bbox':   None,
    # jumlah frame berturut-turut objek tidak terdeteksi
    'misses': 0,
})

# Lock agar inference + update track_history tidak overlap antar request
# mutex supaya 2 request kamera tidak race condition
inference_lock = threading.Lock()

# ─── Load Model ───────────────────────────────────────────────────────────────
# placeholder model YOLO sebelum di-load
model_yolo = None
# placeholder model Keras sebelum di-load
model_keras = None
# mencatat path YOLO mana yang berhasil dimuat
yolo_path_used = None


def load_models():
    # ubah variabel global, bukan lokal
    global model_yolo, model_keras, yolo_path_used

    # Load YOLOv8
    for yolo_path in YOLO_CANDIDATES:                          # coba tiap kandidat path YOLO secara berurutan
        # hanya proses jika file benar-benar ada
        if os.path.exists(yolo_path):
            try:
                # type: ignore  # import lazy supaya start lebih cepat jika tak dipakai
                from ultralytics import YOLO
                # load bobot model YOLO dari file .pt
                model_yolo = YOLO(yolo_path)
                # pindahkan model ke GPU/CPU sesuai deteksi device
                model_yolo.to(YOLO_DEVICE)
                # simpan path yang berhasil dipakai
                yolo_path_used = yolo_path
                print(
                    f"[OK] YOLOv8 model loaded: {yolo_path} (device={YOLO_DEVICE})")
                # berhenti setelah satu model berhasil dimuat
                break
            except Exception as e:
                # log error, lanjut coba kandidat berikutnya
                print(f"[X] YOLOv8 load error ({yolo_path}): {e}")

    if not model_yolo:
        # info jika semua kandidat gagal
        print("[!] YOLOv8 model tidak ditemukan - camera akan pakai demo mode")

    # Load Keras model
    # cek file model klasifikasi ada
    if os.path.exists(MODEL_PATH_KERAS):
        try:
            import tensorflow as tf                            # import lazy TensorFlow
            model_keras = tf.keras.models.load_model(
                MODEL_PATH_KERAS)  # load model MobileNetV2 (.keras)
            print(f"[OK] Keras model loaded: {MODEL_PATH_KERAS}")
        except Exception as e:
            # log error tanpa menghentikan server
            print(f"[X] Keras load error: {e}")
    else:
        print("[!] Keras model tidak ditemukan - klasifikasi akan pakai demo mode")


def preprocess_image(img_array):
    # FIX: model Keras (MobileNetV2) dilatih dengan ImageDataGenerator/PIL yang
    # membaca gambar sebagai RGB. img_array di sini datang dari cv2.imdecode()
    # yang formatnya BGR — kalau tidak dikonversi, kanal merah & biru tertukar
    # saat inference (mismatch dengan training), bisa menurunkan akurasi
    # prediksi secara diam-diam tanpa error apa pun.
    # konversi BGR (OpenCV) → RGB (sesuai training)
    img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    # resize ke 224x224 sesuai input MobileNetV2
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    # normalisasi pixel ke rentang 0–1
    img = img.astype(np.float32) / 255.0
    # tambah dimensi batch → shape (1, 224, 224, 3)
    return np.expand_dims(img, axis=0)


def predict_keras(img_array):
    # preprocessing gambar sebelum masuk model
    processed = preprocess_image(img_array)
    # jalankan inference, ambil hasil batch ke-0
    predictions = model_keras.predict(processed, verbose=0)[0]
    # index kelas dengan probabilitas tertinggi
    pred_idx = int(np.argmax(predictions))
    # nilai confidence kelas terpilih
    confidence = float(predictions[pred_idx])
    all_scores = {CLASS_NAMES_KERAS[i]: float(predictions[i]) for i in range(
        len(CLASS_NAMES_KERAS))}  # skor semua kelas
    # label, confidence, dan semua skor
    return CLASS_NAMES_KERAS[pred_idx], confidence, all_scores


def allowed_file(filename, mimetype):
    ext_ok = os.path.splitext(filename)[1].lower(
    ) in ALLOWED_EXTENSIONS  # cek ekstensi file valid
    mime_ok = mimetype in ALLOWED_MIME_TYPES                    # cek MIME type valid
    # file diterima hanya jika keduanya valid
    return ext_ok and mime_ok


def warmup_models():
    """
    Inferensi pertama setelah model di-load ke GPU biasanya jauh lebih lambat
    (cuDNN/cuda melakukan auto-tuning kernel saat pertama dipanggil). Tanpa
    warmup, USER PERTAMA yang membuka kamera akan kena delay belasan detik itu.
    Warmup di sini "membakar" delay tersebut saat server baru start, bukan
    saat user sedang menunggu.
    """
    dummy = np.zeros(
        (480, 640, 3), dtype=np.uint8)             # gambar hitam dummy untuk pemanasan model

    if model_yolo:
        try:
            t0 = time.time()                                     # catat waktu mulai warmup
            model_yolo.predict(dummy, imgsz=YOLO_IMGSZ_CAMERA, device=YOLO_DEVICE,
                               half=YOLO_HALF, verbose=False)    # jalankan satu inference dummy
            print(
                f"[OK] YOLOv8 warmup selesai ({round((time.time()-t0)*1000)}ms)")
        except Exception as e:
            # warmup gagal tidak fatal, lanjut start server
            print(f"[!] YOLOv8 warmup gagal (diabaikan): {e}")

    if model_keras:
        try:
            # catat waktu mulai warmup Keras
            t0 = time.time()
            # jalankan satu inference dummy
            predict_keras(dummy)
            print(
                f"[OK] Keras warmup selesai ({round((time.time()-t0)*1000)}ms)")
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
        # tidak ada box → langsung kembalikan list kosong
        return raw_boxes

    # luas total frame, dipakai untuk filter rasio area
    frame_area = frame_w * frame_h
    filtered = []
    for b in raw_boxes:
        # koordinat bbox dari tuple deteksi
        bx1, by1, bx2, by2 = b[4], b[5], b[6], b[7]
        # hitung luas bbox
        area = (bx2 - bx1) * (by2 - by1)
        if area <= 0:
            # buang bbox tidak valid (area nol/negatif)
            continue
        # rasio luas bbox terhadap frame
        ratio = area / frame_area
        # Hapus bbox yang terlalu kecil (< 0.5% frame) atau terlalu besar (> 80% frame)
        if ratio < 0.005 or ratio > 0.80:
            # buang noise kecil atau bbox sebesar background
            continue
        # bbox valid, masuk daftar kandidat NMS
        filtered.append(b)

    if len(filtered) <= 1:
        # 0 atau 1 box tidak perlu NMS
        return filtered

    # Sort by conf descending
    # urutkan: confidence tertinggi diproses dulu
    filtered = sorted(filtered, key=lambda b: b[0], reverse=True)
    # daftar box yang lolos (final)
    keep = []
    # index box yang sudah ditekan/dihapus
    suppressed = set()
    for i, b in enumerate(filtered):
        if i in suppressed:
            continue                                               # box ini sudah ditekan, skip
        # box dengan conf tertinggi yang belum ditekan → simpan
        keep.append(b)
        bx1, by1, bx2, by2 = b[4], b[5], b[6], b[7]
        # luas box acuan saat ini
        area_b = (bx2-bx1)*(by2-by1)
        for j, b2 in enumerate(filtered[i+1:], i+1):
            if j in suppressed:
                # box pembanding sudah ditekan, skip
                continue
            ax1, ay1, ax2, ay2 = b2[4], b2[5], b2[6], b2[7]
            # luas box pembanding
            area_b2 = (ax2-ax1)*(ay2-ay1)
            ix1 = max(bx1, ax1)
            # koordinat kiri-atas area overlap
            iy1 = max(by1, ay1)
            ix2 = min(bx2, ax2)
            # koordinat kanan-bawah area overlap
            iy2 = min(by2, ay2)
            iw = max(0, ix2 - ix1)
            # lebar & tinggi overlap (0 jika tak overlap)
            ih = max(0, iy2 - iy1)
            # luas area overlap (intersection)
            inter = iw * ih
            # luas gabungan dua box (union)
            union = area_b + area_b2 - inter
            # IoU standar
            # rasio intersection/union
            iou = inter / union if union > 0 else 0
            # IoMin: overlap dibagi area yang lebih kecil (deteksi bbox kecil di dalam bbox besar)
            # rasio overlap thd box terkecil
            iomin = inter / \
                min(area_b, area_b2) if min(area_b, area_b2) > 0 else 0
            if iou > iou_thresh or iomin > 0.75:
                # box dianggap duplikat → ditekan/dihapus
                suppressed.add(j)
    # hasil akhir box setelah NMS
    return keep

# ─── Error Handlers ───────────────────────────────────────────────────────────


@app.errorhandler(413)
def file_too_large(e):
    # respons saat upload > MAX_CONTENT_LENGTH
    return jsonify({'error': 'Ukuran file terlalu besar (maksimal 10MB).'}), 413


@app.errorhandler(404)
def not_found(e):
    # respons JSON untuk route yang tidak ada
    return jsonify({'error': 'Endpoint tidak ditemukan'}), 404


@app.errorhandler(500)
def server_error(e):
    # respons JSON untuk error tak terduga
    return jsonify({'error': 'Terjadi kesalahan internal pada server'}), 500


# ─── API Routes ───────────────────────────────────────────────────────────────
# Semua route di bawah mengembalikan JSON. HTML/frontend dikelola oleh
# React (Vite) di folder frontend/ — Flask tidak lagi meng-serve HTML.

@app.route('/api/test-upload', methods=['GET'])
def test_upload():
    import cloudinary.uploader
    from dotenv import load_dotenv
    import os
    
    try:
        # Kita buat gambar dummy kosong 1x1 pixel BGR untuk di-upload
        import numpy as np
        import cv2
        dummy_img = np.zeros((1, 1, 3), dtype=np.uint8)
        _, buffer = cv2.imencode('.png', dummy_img)
        img_bytes = buffer.tobytes()
        
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
        if not cloud_name:
            return jsonify({"status": "error", "message": "Secret CLOUDINARY_CLOUD_NAME kosong atau tidak terdeteksi di Hugging Face!"})
            
        res = cloudinary.uploader.upload(img_bytes, folder="smartwaste_scans")
        return jsonify({
            "status": "success", 
            "url": res.get('secure_url'),
            "cloud_name_used": cloud_name
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/api/predict', methods=['POST'])
def predict():
    print("--- [DEBUG] Permintaan API diterima! ---", flush=True)

    if 'image' not in request.files:
        # request tidak menyertakan field 'image'
        return jsonify({'error': 'Tidak ada file gambar'}), 400

    # ambil file upload dari form-data
    file = request.files['image']
    if file.filename == '':
        # field ada tapi nama file kosong
        return jsonify({'error': 'Tidak ada file dipilih'}), 400

    if not allowed_file(file.filename, file.mimetype):
        # validasi tipe file
        return jsonify({'error': 'Format file tidak didukung. Gunakan JPG, PNG, atau WEBP.'}), 400

    # baca seluruh isi file sebagai bytes
    img_bytes = file.read()
    # ubah bytes jadi array uint8
    nparr = np.frombuffer(img_bytes, np.uint8)
    # decode array jadi gambar OpenCV (BGR)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img_bgr is None:
        # file bukan gambar valid / corrupt
        return jsonify({'error': 'Gagal membaca gambar'}), 400

    if not model_keras:
        # model belum dimuat
        return jsonify({'error': 'Model klasifikasi tidak tersedia. Pastikan file model sudah ada di ../model/classification/.'}), 503

    try:
        label, confidence, all_scores = predict_keras(
            img_bgr)     # jalankan klasifikasi MobileNetV2
        # label model yang dipakai, untuk response
        model_used = 'MobileNetV2'
    except Exception as e:
        # tangani error saat inference
        return jsonify({'error': f'Prediksi gagal: {str(e)}'}), 500

    # ─── Confidence threshold — tolak prediksi yang tidak meyakinkan ──────
    # Jika skor tertinggi model < CONFIDENCE_THRESHOLD (60%), gambar yang
    # diupload kemungkinan bukan sampah yang dikenal model. Daripada memaksa
    # ke salah satu kelas, label diubah ke "Tidak Dikenali" dan rekomendasi
    # dikosongkan agar frontend tidak menampilkan tips yang menyesatkan.
    if confidence < CONFIDENCE_THRESHOLD:
        label = 'Tidak Dikenali'
        rec = {
            'icon':   '❓',
            'color':  '#6b7280',                                     # warna netral abu-abu
            'tips':   ['Tolong unggah gambar sampah yang lebih jelas.'],
            'action': 'Tidak Dikenali',
        }
    else:
        # ambil data rekomendasi sesuai label prediksi
        rec = RECOMMENDATIONS.get(label, {})

    # ─── Upload ke Cloudinary (background, tidak menunda response) ────────
    # ambil ekstensi file asli
    ext = os.path.splitext(file.filename)[1].lower()
    # nama file unik berbasis waktu
    cloudinary_filename = f"{datetime.now():%Y%m%d_%H%M%S}_{int(time.time()*1000)}{ext}"

    def _log_cloudinary_upload(public_id, public_url):
        if public_url:                                               # hanya log jika upload Cloudinary berhasil
            entry = {
                'filename':   cloudinary_filename,
                'cloudinary_id': public_id,
                'file_url': public_url,
                # label sudah di-override jika di bawah threshold
                'prediction': label,
                'confidence': round(confidence * 100, 1),
                'timestamp':  datetime.now().isoformat(),
            }
            # append entry sebagai satu baris JSON
            with open('riwayat.jsonl', 'a') as f:
                f.write(json.dumps(entry) + '\n')

    upload_to_cloudinary_async(
        img_bytes,
        cloudinary_filename,
        on_done=_log_cloudinary_upload
    )  # upload async, callback saat selesai

    return jsonify({
        'success':        True,
        # kelas hasil prediksi (atau "Tidak Dikenali")
        'prediction':     label,
        # confidence model mentah dalam persen
        'confidence':     round(confidence * 100, 1),
        'all_scores':     {k: round(v * 100, 1) for k, v in
                           sorted(all_scores.items(), key=lambda x: x[1], reverse=True)},  # semua skor, diurutkan desc
        # ikon, warna, tips, dan aksi (kosong jika tidak dikenali)
        'recommendation': rec,
        # info model yang dipakai
        'model_used':     model_used,
    })


@app.route('/api/camera-frame', methods=['POST'])
def camera_frame():
    # ambil body JSON dari request
    data = request.get_json()
    if not data or 'frame' not in data:
        # body tidak valid / field frame tidak ada
        return jsonify({'error': 'No frame data'}), 400

    try:
        # buang prefix "data:image/...;base64,"
        frame_data = data['frame'].split(',')[1]
        # decode base64 → bytes gambar
        frame_bytes = base64.b64decode(frame_data)
        # bytes → array uint8
        nparr = np.frombuffer(frame_bytes, np.uint8)
        # decode array → gambar OpenCV (BGR)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            # gambar gagal didecode
            raise ValueError('cv2.imdecode returned None')
    except Exception as e:
        # tangani semua error decoding frame
        return jsonify({'error': f'Frame decode error: {str(e)}'}), 400

    # FIX: ambil resolusi frame dari client agar scaling bbox akurat
    # lebar frame asli dari sisi client
    send_w = int(data.get('send_w', frame.shape[1]))
    # tinggi frame asli dari sisi client
    send_h = int(data.get('send_h', frame.shape[0]))

    # mulai hitung waktu inferensi
    t_start = time.time()
    # list hasil deteksi yang akan dikirim ke client
    detections = []

    if model_yolo:
        try:
            # track_id yang muncul di frame ini
            current_ids = set()

            with inference_lock:                                         # cegah race condition antar request paralel
                try:
                    # Tracking aktif → setiap objek punya track_id konsisten antar-frame
                    results = model_yolo.track(
                        frame,
                        conf=YOLO_CONF,                              # ambang minimum confidence deteksi
                        iou=YOLO_IOU,                                # ambang IoU untuk NMS internal YOLO
                        imgsz=YOLO_IMGSZ_CAMERA,                       # resolusi input inference
                        persist=True,                                    # pertahankan track_id antar frame
                        # algoritma tracking yang dipakai
                        tracker='bytetrack.yaml',
                        # nonaktifkan log bawaan ultralytics
                        verbose=False,
                        # device inference (GPU/CPU)
                        device=YOLO_DEVICE,
                        half=YOLO_HALF,                                # gunakan FP16 jika di GPU
                        max_det=5,                                        # batas maksimal objek per frame
                    )
                except Exception:
                    # Fallback jika dependency tracker ('lap'/'lapx') belum terpasang
                    results = model_yolo.predict(
                        frame,
                        conf=YOLO_CONF,
                        iou=YOLO_IOU,
                        imgsz=YOLO_IMGSZ_CAMERA,
                        verbose=False,
                        device=YOLO_DEVICE,
                        half=YOLO_HALF,
                        max_det=5,
                    )                                                       # mode tanpa tracking (tanpa track_id)

                # Kumpulkan raw boxes dulu, lalu NMS lintas kelas
                # penampung semua bbox mentah hasil model
                raw_boxes = []
                for result in results:
                    # objek bbox hasil dari satu frame
                    boxes = result.boxes
                    if boxes is None or len(boxes) == 0:
                        # tidak ada objek terdeteksi, lanjut
                        continue
                    for box in boxes:
                        # id kelas hasil deteksi
                        cls_id = int(box.cls[0])
                        # confidence deteksi
                        conf = float(box.conf[0])
                        # koordinat bbox (format xyxy)
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        # clamp koordinat agar tidak keluar frame
                        x1 = max(0, min(int(x1), send_w))
                        y1 = max(0, min(int(y1), send_h))
                        x2 = max(0, min(int(x2), send_w))
                        y2 = max(0, min(int(y2), send_h))
                        if (x2 - x1) < 20 or (y2 - y1) < 20:
                            # buang bbox terlalu kecil (noise)
                            continue
                        # mapping id kelas → nama Indonesia
                        label = YOLO_CLASS_MAP.get(cls_id, f'Kelas {cls_id}')
                        # ambil track_id jika tracking aktif
                        track_id = int(
                            box.id[0]) if box.id is not None else None
                        # simpan sebagai tuple
                        raw_boxes.append(
                            (conf, cls_id, label, track_id, x1, y1, x2, y2))

                # NMS lintas kelas dengan area filter dan IoMin
                # bersihkan duplikat antar kelas
                raw_boxes = _nms_detections(
                    raw_boxes, iou_thresh=0.45, frame_w=send_w, frame_h=send_h)

                for (conf, cls_id, label, track_id, x1, y1, x2, y2) in raw_boxes:
                    if track_id is None:
                        # Tracker non-aktif (fallback predict) → filter conf lalu tampilkan
                        if conf < MIN_CONF_DISPLAY:
                            # confidence terlalu rendah, jangan tampilkan
                            continue
                        # ambil data rekomendasi sesuai label
                        rec = RECOMMENDATIONS.get(label, {})
                        detections.append({
                            'label':      label,
                            'confidence': round(conf * 100, 1),
                            'bbox':       [x1, y1, x2, y2],
                            'color':      rec.get('color', '#10d9a0'),
                            'icon':       rec.get('icon', '♻️'),
                            'action':     rec.get('action', 'Pisahkan'),
                        })
                        continue                                        # lanjut ke box berikutnya

                    # tandai track_id ini aktif di frame ini
                    current_ids.add(track_id)
                    # ambil/buat riwayat untuk track_id ini
                    hist = track_history[track_id]
                    # simpan label terbaru ke antrian
                    hist['labels'].append(label)
                    # simpan confidence terbaru ke antrian
                    hist['confs'].append(conf)
                    # update posisi bbox terakhir
                    hist['bbox'] = [x1, y1, x2, y2]
                    # reset hitungan frame hilang
                    hist['misses'] = 0

                # ── Majority voting + confidence averaging + hold-last detection ──
                # iterasi semua track_id yang pernah tercatat
                for tid in list(track_history.keys()):
                    hist = track_history[tid]

                    if tid not in current_ids:
                        # objek tidak terdeteksi di frame ini
                        hist['misses'] += 1
                        if hist['misses'] > HOLD_FRAMES:
                            # sudah lewat batas toleransi → hapus riwayat
                            del track_history[tid]
                            continue
                        # masih dalam toleransi, tetap tunggu frame berikut
                        continue

                    if not hist['labels']:
                        # belum ada data label tersimpan, skip
                        continue

                    # Weighted voting: setiap label diboboti dengan confidence-nya
                    # → label dengan conf tinggi lebih dominan meskipun jumlah frame sama
                    # akumulator skor tiap label
                    weighted_scores = defaultdict(float)
                    for lbl, cf in zip(hist['labels'], hist['confs']):
                        # tambahkan confidence ke skor labelnya
                        weighted_scores[lbl] += cf
                    # label dengan skor tertinggi
                    stable_label = max(
                        weighted_scores, key=weighted_scores.get)
                    # rata-rata confidence beberapa frame terakhir
                    avg_conf = sum(hist['confs']) / len(hist['confs'])

                    # Jangan tampilkan jika confidence rata-rata terlalu rendah
                    if avg_conf < MIN_CONF_DISPLAY:
                        # confidence rata-rata di bawah threshold, skip
                        continue

                    # ambil rekomendasi sesuai label stabil
                    rec = RECOMMENDATIONS.get(stable_label, {})
                    detections.append({
                        'label':      stable_label,
                        'confidence': round(avg_conf * 100, 1),
                        'bbox':       hist['bbox'],
                        'color':      rec.get('color', '#10d9a0'),
                        'icon':       rec.get('icon', '♻️'),
                        'action':     rec.get('action', 'Pisahkan'),
                    })

        except Exception as e:
            # error inference, tetap balas 200 agar client tidak crash
            return jsonify({'error': f'YOLO error: {str(e)}', 'detections': []}), 200
    else:
        # model YOLO belum dimuat
        return jsonify({'error': 'Model deteksi tidak tersedia. Pastikan file model sudah ada di ../model/yolo/.'}), 503

    # total waktu proses frame ini (ms)
    inference_ms = round((time.time() - t_start) * 1000)
    device_label = 'GPU' if (isinstance(YOLO_DEVICE, int) or str(
        YOLO_DEVICE).startswith('cuda')) else 'CPU'  # label device untuk ditampilkan
    return jsonify({
        'success':      True,
        # daftar objek terdeteksi
        'detections':   detections,
        # waktu inferensi
        'inference_ms': inference_ms,
        # info model & device yang dipakai
        'model':        f'YOLOv8m ({device_label})',
    })


@app.route('/api/status')
def status():
    device_label = 'GPU' if (isinstance(YOLO_DEVICE, int) or str(
        YOLO_DEVICE).startswith('cuda')) else 'CPU'  # device aktif saat ini
    return jsonify({
        # status model Keras sudah dimuat atau belum
        'keras_model':   model_keras is not None,
        # status model YOLO sudah dimuat atau belum
        'yolo_model':    model_yolo is not None,
        # path file YOLO yang dipakai
        'yolo_path':     yolo_path_used,
        # device yang dipakai YOLO
        'yolo_device':   device_label,
        # daftar kelas Keras
        'classes_keras': CLASS_NAMES_KERAS,
        # daftar kelas YOLO
        'classes_yolo':  list(YOLO_CLASS_MAP.values()),
        # duplikat info (kompatibilitas frontend lama)
        'keras_loaded':  model_keras is not None,
        # duplikat info (kompatibilitas frontend lama)
        'yolo_loaded':   model_yolo is not None,
    })


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # muat semua model AI sebelum server jalan
    load_models()
    # lakukan inference dummy agar request pertama tidak lambat
    warmup_models()

    # DEBUG_MODE dikontrol lewat environment variable, default OFF.
    # PENTING: debug=True mengaktifkan Werkzeug debugger interaktif yang bisa
    # dieksploitasi untuk remote code execution kalau server ini diakses dari
    # luar jaringan lokal (mis. lewat ngrok atau deploy ke cloud). Jangan
    # pernah nyalakan DEBUG_MODE=1 kalau host bisa diakses publik.
    #   Windows  : set DEBUG_MODE=1 && python app.py
    #   Linux/Mac: DEBUG_MODE=1 python app.py
    # baca flag debug dari environment
    DEBUG_MODE = os.environ.get('DEBUG_MODE', '0') == '1'

    # use_reloader=False supaya load_models()/warmup_models() tidak terpanggil
    # dua kali (sebelumnya proses parent+child Werkzeug reloader masing-masing
    # memuat model, kontributor lonjakan delay di awal start).
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=5000,
            threaded=True, use_reloader=False)  # jalankan server Flask
