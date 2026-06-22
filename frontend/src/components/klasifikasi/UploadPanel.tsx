import { useRef, useState, useCallback } from 'react';
import { ALLOWED_MIME_TYPES, MAX_FILE_SIZE } from '../../lib/constants';

interface UploadPanelProps {
  onFileSelect: (file: File) => void;
  onPredict: () => void;
  selectedFile: File | null;
  isPredicting: boolean;
}

export function UploadPanel({ onFileSelect, onPredict, selectedFile, isPredicting }: UploadPanelProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);

  const handleFile = useCallback((file: File) => {
    if (!ALLOWED_MIME_TYPES.includes(file.type)) {
      alert('Format tidak didukung. Gunakan JPG, PNG, atau WEBP.');
      return;
    }
    if (file.size > MAX_FILE_SIZE) {
      alert('Ukuran file maksimal 10MB.');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => setPreviewUrl(e.target?.result as string);
    reader.readAsDataURL(file);
    onFileSelect(file);
  }, [onFileSelect]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
  }, [handleFile]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) handleFile(e.target.files[0]);
  };

  return (
    <div className="panel upload-panel fade-up">
      <div className="panel-header">
        <span className="panel-dot"></span>
        UPLOAD GAMBAR
      </div>

      <div
        className={`dropzone ${isDragOver ? 'drag-over' : ''}`}
        tabIndex={0}
        role="button"
        aria-label="Upload gambar sampah"
        onClick={() => fileInputRef.current?.click()}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInputRef.current?.click();
          }
        }}
        onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
      >
        <div className="dz-icon">
          <svg viewBox="0 0 24 24" fill="none"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><polyline points="17 8 12 3 7 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><line x1="12" y1="3" x2="12" y2="15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/></svg>
        </div>
        <p className="dz-title">Drag &amp; Drop gambar di sini</p>
        <p className="dz-hint">atau klik untuk browse file</p>
        <p className="dz-meta">JPG &middot; PNG &middot; WEBP &nbsp;|&nbsp; Maks 10MB</p>
        <label className="btn-ghost btn-sm dz-btn" onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}>
          Pilih File
        </label>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          hidden
          onChange={handleInputChange}
        />
      </div>

      <div className="preview-label">PREVIEW</div>
      <div className="preview-box">
        {!previewUrl ? (
          <span className="preview-placeholder">Gambar akan tampil di sini setelah diunggah</span>
        ) : (
          <img src={previewUrl} alt="Preview gambar sampah" style={{ display: 'block' }} />
        )}
      </div>

      <button className="btn-primary btn-full" onClick={onPredict} disabled={!selectedFile || isPredicting}>
        <svg viewBox="0 0 24 24" fill="none"><path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z" fill="currentColor"/></svg>
        Prediksi Sekarang
      </button>
    </div>
  );
}
