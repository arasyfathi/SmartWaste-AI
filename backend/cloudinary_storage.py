import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Memuat kunci rahasia dari file .env
load_dotenv()

# Konfigurasi otomatis menggunakan environment variables
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)


def upload_to_cloudinary(image_path):
    """
    Mengunggah gambar ke Cloudinary dan mengembalikan URL publiknya.
    Gambar akan dimasukkan ke folder 'smartwaste_scans' di akun Cloudinary-mu.
    """
    try:
        # Proses unggah
        response = cloudinary.uploader.upload(
            image_path,
            folder="smartwaste_scans"  # Nama folder di Cloudinary
        )

        # Mengambil URL HTTPS yang aman
        secure_url = response.get('secure_url')
        print(f"[OK] Gambar berhasil diunggah: {secure_url}")
        return secure_url

    except Exception as e:
        print(f"[ERROR] Gagal mengunggah ke Cloudinary: {e}")
        return None
