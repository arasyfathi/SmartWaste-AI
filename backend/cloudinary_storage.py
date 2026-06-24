import os
import threading
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Memuat kunci rahasia dari file .env (lokal)
# Di Hugging Face, secrets otomatis tersedia sebagai env vars
load_dotenv()

# Konfigurasi otomatis menggunakan environment variables
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)


def _upload_worker(img_bytes, filename, on_done):
    """Fungsi pekerja yang berjalan di background thread untuk mengunggah gambar."""
    try:
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
        api_key = os.getenv('CLOUDINARY_API_KEY')
        api_secret = os.getenv('CLOUDINARY_API_SECRET')

        print(f"[Cloudinary] Memulai upload: {filename}, cloud_name={cloud_name}", flush=True)

        if not cloud_name or not api_key or not api_secret:
            print("[X] Gagal upload: Kredensial Cloudinary tidak lengkap!", flush=True)
            if on_done:
                on_done(None, None)
            return

        # Re-konfigurasi di setiap upload untuk memastikan credentials selalu fresh
        # (penting di Docker/Gunicorn multi-thread environment)
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )

        # Menghapus ekstensi file untuk dijadikan public_id di Cloudinary
        public_id_base = os.path.splitext(filename)[0]

        # Unggah langsung data bytes gambar tanpa perlu disimpan ke disk dahulu
        response = cloudinary.uploader.upload(
            img_bytes,
            public_id=public_id_base,
            folder="smartwaste_scans"
        )

        public_id = response.get('public_id')
        secure_url = response.get('secure_url')

        print(f"[OK] Cloudinary upload berhasil: {secure_url}", flush=True)

        # Jalankan fungsi callback untuk mencatat riwayat ke JSONL
        if on_done:
            on_done(public_id, secure_url)

    except Exception as e:
        print(f"[X] Gagal mengunggah ke Cloudinary: {e}", flush=True)
        if on_done:
            on_done(None, None)


def upload_to_cloudinary_async(img_bytes, filename, on_done=None):
    """
    Memulai proses unggah di thread terpisah agar Flask tidak mengalami
    flicker/lag saat melayani request frame kamera atau upload.

    daemon=False memastikan thread selesai sebelum proses Python berhenti,
    penting di lingkungan Gunicorn/Docker agar upload tidak terputus di tengah jalan.
    """
    thread = threading.Thread(
        target=_upload_worker,
        args=(img_bytes, filename, on_done),
        daemon=False  # PENTING: False agar Gunicorn tidak membunuh thread sebelum upload selesai
    )
    thread.start()
