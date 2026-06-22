import { useCamera } from '../hooks/useCamera';
import { EmojiToIcon, LightbulbIcon } from '../lib/icons';

export function Camera() {
  const {
    videoRef,
    canvasRef,
    isRunning,
    fps,
    aiRate,
    objectCount,
    inferenceMs,
    detections,
    startCamera,
    stopCamera,
    flipCamera,
    takeScreenshot,
  } = useCamera();

  return (
    <>
      <section className="page-hero">
        <div className="orb orb-2" style={{ top: '-180px', left: '-120px', opacity: 0.35 }}></div>
        <h1 className="page-title">Deteksi Sampah <span className="accent">Real-Time</span></h1>
        <p className="page-sub">Arahkan kamera ke sampah dan YOLOv8 akan mengidentifikasinya secara langsung</p>
        <div className="divider-line"></div>
      </section>

      <div className="camera-layout">
        {/* Camera Feed Panel */}
        <div className="panel camera-panel fade-up">
          <div className="camera-topbar">
            <span className={`live-dot ${isRunning ? 'active' : ''}`}></span>
            <span className="live-text">{isRunning ? 'LIVE' : 'SIAP'}</span>
            <span className="cam-meta">YOLOv8 &middot; SmartWaste AI</span>
            <span className="cam-fps">
              {isRunning && fps > 0 ? `Render ${fps} FPS \u00B7 AI ~${aiRate}/s` : ''}
            </span>
          </div>

          <div className="video-wrap">
            <video ref={videoRef} autoPlay playsInline muted></video>
            <canvas ref={canvasRef}></canvas>
            {!isRunning && (
              <div className="cam-placeholder">
                <svg viewBox="0 0 24 24" fill="none"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/><circle cx="12" cy="13" r="3.5" fill="currentColor" opacity="0.4"/></svg>
                <p>Klik <strong>Mulai Kamera</strong> untuk memulai deteksi real-time</p>
              </div>
            )}
          </div>

          <div className="camera-bottombar">
            <span>{objectCount} Objek Terdeteksi</span>
            <span>{inferenceMs !== null ? `Waktu Inferensi (server): ${inferenceMs}ms` : ''}</span>
          </div>
        </div>

        {/* Detection Results Panel */}
        <div className="panel det-panel fade-up fade-up-delay-1">
          <div className="panel-header">
            <span className="panel-dot"></span>
            HASIL DETEKSI
            <span className="status-badge">Real-time</span>
          </div>
          <div className="det-list">
            {detections.length === 0 ? (
              <div className="det-empty">
                <svg viewBox="0 0 24 24" fill="none"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/><circle cx="12" cy="13" r="3.5" fill="currentColor" opacity="0.3"/></svg>
                {!isRunning
                  ? 'Belum ada objek terdeteksi.\nMulai kamera untuk memulai.'
                  : 'Tidak ada objek terdeteksi saat ini.'}
              </div>
            ) : (
              detections.map((det, i) => {
                const color = det.color || '#5ba35b';
                return (
                  <div key={i} className="det-item">
                    <div className="det-item-top">
                      <span className="det-item-icon" style={{ color }}>
                        <EmojiToIcon emoji={det.icon} />
                      </span>
                      <span className="det-item-name">{det.label}</span>
                      <span className="det-item-conf" style={{ color }}>{det.confidence}%</span>
                    </div>
                    <div className="det-bar-track">
                      <div className="det-bar-fill" style={{ background: color, width: `${det.confidence}%` }}></div>
                    </div>
                    <div className="det-item-action">
                      <LightbulbIcon /> {det.action || 'Pisahkan ke tempat sampah yang sesuai'}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>

      {/* Camera Controls */}
      <div className="cam-controls fade-up fade-up-delay-2">
        <button className="btn-primary" onClick={startCamera} disabled={isRunning}>
          <svg viewBox="0 0 24 24" fill="none"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/><circle cx="12" cy="13" r="3.5" fill="currentColor" opacity="0.4"/></svg>
          Mulai Kamera
        </button>
        <button className="btn-danger" onClick={stopCamera} disabled={!isRunning}>
          <svg viewBox="0 0 24 24" fill="none"><rect x="6" y="6" width="12" height="12" rx="2" fill="currentColor"/></svg>
          Stop Kamera
        </button>
        <button className="btn-ghost" onClick={takeScreenshot} disabled={!isRunning}>
          <svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" strokeWidth="2"/><circle cx="9" cy="9" r="2" fill="currentColor" opacity="0.5"/><path d="m21 15-5-5L5 21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
          Screenshot
        </button>
        <button className="btn-ghost" onClick={flipCamera} disabled={!isRunning}>
          <svg viewBox="0 0 24 24" fill="none"><path d="M3 12a9 9 0 0 1 15.5-6.36L21 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M21 3v5h-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M21 12a9 9 0 0 1-15.5 6.36L3 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M3 21v-5h5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
          Ganti Kamera
        </button>
      </div>

      {/* How It Works Strip */}
      <div className="how-strip fade-up fade-up-delay-3">
        <h3 className="how-strip-title">Cara Kerja Deteksi Real-Time</h3>
        <div className="how-steps">
          {[
            { num: '01', icon: <svg viewBox="0 0 24 24" fill="none"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/><circle cx="12" cy="13" r="3.5" fill="currentColor" opacity="0.4"/></svg>, title: 'Akses Kamera', desc: 'WebRTC mengakses kamera browser' },
            { num: '02', icon: <svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" strokeWidth="2"/><circle cx="9" cy="9" r="2" fill="currentColor" opacity="0.5"/><path d="m21 15-5-5L5 21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>, title: 'Capture Frame', desc: 'Canvas API mengambil frame setiap 30fps' },
            { num: '03', icon: <svg viewBox="0 0 24 24" fill="none"><path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z" fill="currentColor"/></svg>, title: 'YOLOv8 Inferensi', desc: 'Model deteksi objek real-time via OpenCV' },
            { num: '04', icon: <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2"/><circle cx="12" cy="12" r="5" stroke="currentColor" strokeWidth="2"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>, title: 'Bounding Box', desc: 'Overlay bounding box + label + confidence' },
            { num: '05', icon: <svg viewBox="0 0 24 24" fill="none"><path d="M3 3v16a2 2 0 0 0 2 2h16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><rect x="7" y="13" width="3" height="5" rx="1" fill="currentColor"/><rect x="12" y="9" width="3" height="9" rx="1" fill="currentColor" opacity="0.6"/><rect x="17" y="5" width="3" height="13" rx="1" fill="currentColor" opacity="0.85"/></svg>, title: 'Tampilkan Hasil', desc: 'Update panel deteksi secara live' },
          ].map((step, i) => (
            <div key={step.num}>
              {i > 0 && <div className="how-arrow">&rarr;</div>}
              <div className="how-step">
                <div className="how-step-num">{step.num}</div>
                <div className="how-step-icon">{step.icon}</div>
                <strong>{step.title}</strong>
                <p>{step.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
