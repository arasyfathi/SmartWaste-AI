import os
import io
import time
import socket
import threading
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive.file']
TOKEN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.json')
DRIVE_FOLDER_ID = os.environ.get('DRIVE_FOLDER_ID')

MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2

_drive_service = None
_lock = threading.Lock()


def _get_service(force_refresh=False):
    global _drive_service
    if _drive_service and not force_refresh:
        return _drive_service
    with _lock:
        if _drive_service and not force_refresh:
            return _drive_service
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_PATH, 'w') as f:
                f.write(creds.to_json())
        _drive_service = build('drive', 'v3', credentials=creds)
        return _drive_service


def _is_retryable(e):
    """True kalau error-nya kemungkinan cuma glitch sesaat (worth di-retry)."""
    if isinstance(e, (socket.timeout, ConnectionError, OSError, TimeoutError)):
        return True
    if isinstance(e, HttpError):
        return e.resp.status in (429, 500, 502, 503, 504)
    return False


def upload_to_drive(file_bytes, filename, mimetype='image/jpeg'):
    """Upload bytes gambar ke Google Drive, dengan retry otomatis."""
    if not os.path.exists(TOKEN_PATH):
        print(f"[!] token.json tidak ditemukan di {TOKEN_PATH} — skip upload ke Drive")
        return None, None

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            service = _get_service()
            metadata = {'name': filename}
            if DRIVE_FOLDER_ID:
                metadata['parents'] = [DRIVE_FOLDER_ID]
            media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype=mimetype)
            file = service.files().create(
                body=metadata, media_body=media, fields='id, webViewLink'
            ).execute()
            print(f"[✓] Uploaded ke Drive: {filename} (percobaan ke-{attempt})")
            return file.get('id'), file.get('webViewLink')

        except Exception as e:
            last_error = e
            retryable = _is_retryable(e)
            print(f"[!] Upload ke Drive gagal (percobaan {attempt}/{MAX_RETRIES}): {e}")

            if not retryable:
                print("[!] Error ini bukan masalah koneksi sesaat — tidak di-retry.")
                break

            if attempt < MAX_RETRIES:
                delay = RETRY_BACKOFF_BASE ** attempt
                print(f"[~] Mencoba lagi dalam {delay} detik...")
                time.sleep(delay)
                _get_service(force_refresh=True)

    print(f"[!] Upload ke Drive gagal total setelah {MAX_RETRIES} percobaan: {last_error}")
    return None, None


def upload_to_drive_async(file_bytes, filename, mimetype='image/jpeg', on_done=None):
    """Upload di background thread (dengan retry built-in)."""
    def _worker():
        file_id, link = upload_to_drive(file_bytes, filename, mimetype)
        if on_done:
            on_done(file_id, link)
    threading.Thread(target=_worker, daemon=True).start()
