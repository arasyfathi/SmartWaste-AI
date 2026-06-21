import os
import io
import threading
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
TOKEN_PATH = 'token.json'
DRIVE_FOLDER_ID = os.environ.get('DRIVE_FOLDER_ID')

_drive_service = None
_lock = threading.Lock()


def _get_service():
    global _drive_service
    if _drive_service:
        return _drive_service
    with _lock:
        if _drive_service:
            return _drive_service
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_PATH, 'w') as f:
                f.write(creds.to_json())
        _drive_service = build('drive', 'v3', credentials=creds)
        return _drive_service


def upload_to_drive(file_bytes, filename, mimetype='image/jpeg'):
    """Upload bytes gambar ke Google Drive. Return (file_id, webViewLink) atau (None, None) kalau gagal."""
    try:
        service = _get_service()
        metadata = {'name': filename}
        if DRIVE_FOLDER_ID:
            metadata['parents'] = [DRIVE_FOLDER_ID]
        media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype=mimetype)
        file = service.files().create(
            body=metadata, media_body=media, fields='id, webViewLink'
        ).execute()
        print(f"[✓] Uploaded ke Drive: {filename}")
        return file.get('id'), file.get('webViewLink')
    except Exception as e:
        print(f"[!] Upload ke Drive gagal (diabaikan): {e}")
        return None, None


def upload_to_drive_async(file_bytes, filename, mimetype='image/jpeg', on_done=None):
    """Upload di background thread — supaya /api/predict tidak nunggu Drive API selesai."""
    def _worker():
        file_id, link = upload_to_drive(file_bytes, filename, mimetype)
        if on_done:
            on_done(file_id, link)
    threading.Thread(target=_worker, daemon=True).start()