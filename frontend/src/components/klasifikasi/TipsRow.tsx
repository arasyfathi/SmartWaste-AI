export function TipsRow() {
  return (
    <div className="tips-row">
      <div className="tip-card fade-up">
        <span className="tip-icon">
          <svg viewBox="0 0 24 24" fill="none"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/><circle cx="12" cy="13" r="3.5" fill="currentColor" opacity="0.4"/></svg>
        </span>
        <div>
          <strong>Pencahayaan Baik</strong>
          <p>Gambar terang dan jelas untuk prediksi optimal.</p>
        </div>
      </div>
      <div className="tip-card fade-up fade-up-delay-1">
        <span className="tip-icon">
          <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2"/><circle cx="12" cy="12" r="5" stroke="currentColor" strokeWidth="2"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>
        </span>
        <div>
          <strong>Satu Objek</strong>
          <p>Foto satu jenis sampah per gambar untuk akurasi terbaik.</p>
        </div>
      </div>
      <div className="tip-card fade-up fade-up-delay-2">
        <span className="tip-icon">
          <svg viewBox="0 0 24 24" fill="none"><path d="M3 12a9 9 0 0 1 15.5-6.36L21 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M21 3v5h-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M21 12a9 9 0 0 1-15.5 6.36L3 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M3 21v-5h5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
        </span>
        <div>
          <strong>Coba Ulang</strong>
          <p>Jika confidence rendah, coba sudut berbeda.</p>
        </div>
      </div>
    </div>
  );
}
