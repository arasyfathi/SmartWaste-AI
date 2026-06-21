// ── SmartWaste AI — camera.js ─────────────────────────────────────────────────

// Map emoji icon dari backend (RECOMMENDATIONS di app.py) ke SVG ikon premium
const EMOJI_TO_SVG = {
  '♻️': `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="8" y="3" width="8" height="3" rx="1" fill="currentColor" opacity="0.5"/><path d="M9 6v2.5L7 11v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-9l-2-2.5V6" stroke="currentColor" stroke-width="2" stroke-linejoin="round" fill="currentColor" fill-opacity="0.12"/><line x1="7.5" y1="14" x2="16.5" y2="14" stroke="currentColor" stroke-width="2"/></svg>`,
  '📄': `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M14 2v6h6" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><line x1="8" y1="13" x2="16" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="8" y1="17" x2="13" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`,
  '📦': `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>`,
  '🪟': `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7 3h10l-1.2 13.5a3.5 3.5 0 0 1-3.49 3.2h-.62a3.5 3.5 0 0 1-3.49-3.2L7 3z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" fill="currentColor" fill-opacity="0.1"/><line x1="7.6" y1="9" x2="16.4" y2="9" stroke="currentColor" stroke-width="2"/></svg>`,
  '⚙️': `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" fill="currentColor" fill-opacity="0.08"/></svg>`,
  '🌿': `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" fill="currentColor" opacity="0.18"/><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 11 13 11 11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
};
const ICON_FALLBACK = EMOJI_TO_SVG['♻️'];
const ICON_LIGHTBULB = `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9 18h6M10 22h4M12 2a6 6 0 0 0-4 10.5c.6.5 1 1.3 1 2.1V15h6v-.4c0-.8.4-1.6 1-2.1A6 6 0 0 0 12 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="currentColor" fill-opacity="0.12"/></svg>`;

function iconFor(emoji) {
  return EMOJI_TO_SVG[emoji] || ICON_FALLBACK;
}

const video       = document.getElementById('cam-video');
const canvas      = document.getElementById('cam-canvas');
const ctx         = canvas.getContext('2d');
const placeholder = document.getElementById('cam-placeholder');

const btnStart = document.getElementById('btn-start');
const btnStop  = document.getElementById('btn-stop');
const btnShot  = document.getElementById('btn-shot');
const btnFlip  = document.getElementById('btn-flip');

const liveDot   = document.querySelector('.live-dot');
const liveText  = document.getElementById('live-text');
const camMeta   = document.getElementById('cam-meta');
const camFps    = document.getElementById('cam-fps');
const objCount  = document.getElementById('obj-count');
const inferTime = document.getElementById('infer-time');
const detList   = document.getElementById('det-list');
const realtimeBadge = document.getElementById('realtime-badge');

let stream        = null;
let animFrame     = null;
let isRunning     = false;
let facingMode    = 'environment';
let lastInfer     = 0;
let inferInterval = 500; // ms antar pemanggilan server, disesuaikan otomatis di bawah
const MIN_INTERVAL = 100;  // jangan lebih cepat dari ini meski server sangat cepat
const MAX_INTERVAL = 2000; // jangan lebih lambat dari ini meski server sangat lambat
let isInferring    = false; // mencegah request baru menumpuk sebelum request sebelumnya selesai
let frameCount    = 0;
let fpsTimer      = 0;
let currentFps    = 0;

const EMPTY_HTML = `<div class="det-empty">
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="12" cy="13" r="3.5" fill="currentColor" opacity="0.3"/></svg>
  Belum ada objek terdeteksi.<br>Mulai kamera untuk memulai.
</div>`;

const NO_OBJECT_HTML = `<div class="det-empty">
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><line x1="16.5" y1="16.5" x2="21" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
  Tidak ada objek terdeteksi saat ini.
</div>`;

// ── Start / stop / flip / screenshot ─────────────────────────────────────────
btnStart.addEventListener('click', startCamera);
btnStop.addEventListener('click', stopCamera);
btnFlip.addEventListener('click', flipCamera);
btnShot.addEventListener('click', takeScreenshot);

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode, width: { ideal: 1280 }, height: { ideal: 720 } },
      audio: false,
    });
    video.srcObject = stream;
    await video.play();

    placeholder.style.display = 'none';
    liveDot.classList.add('active');
    liveText.textContent = 'LIVE';
    camMeta.textContent  = 'YOLOv8 \u00B7 SmartWaste AI';

    btnStart.disabled = true;
    btnStop.disabled  = false;
    btnShot.disabled  = false;
    btnFlip.disabled  = false;

    isRunning = true;
    fpsTimer  = performance.now();
    loop();
  } catch (err) {
    alert('Tidak bisa mengakses kamera: ' + err.message);
  }
}

function stopCamera() {
  isRunning = false;
  if (animFrame) cancelAnimationFrame(animFrame);
  if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }
  video.srcObject = null;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  placeholder.style.display = '';
  liveDot.classList.remove('active');
  liveText.textContent = 'SIAP';
  camMeta.textContent  = 'YOLOv8 \u00B7 SmartWaste AI';
  camFps.textContent   = '';
  objCount.textContent = '0 Objek Terdeteksi';
  inferTime.textContent = '';

  btnStart.disabled = false;
  btnStop.disabled  = true;
  btnShot.disabled  = true;
  btnFlip.disabled  = true;

  detList.innerHTML = EMPTY_HTML;
}

async function flipCamera() {
  facingMode = facingMode === 'environment' ? 'user' : 'environment';
  stopCamera();
  await startCamera();
}

function takeScreenshot() {
  const tmpCanvas = document.createElement('canvas');
  tmpCanvas.width  = video.videoWidth;
  tmpCanvas.height = video.videoHeight;
  tmpCanvas.getContext('2d').drawImage(video, 0, 0);
  const link = document.createElement('a');
  link.download = `smartwaste_${Date.now()}.jpg`;
  link.href = tmpCanvas.toDataURL('image/jpeg', .9);
  link.click();
}

// ── Main loop ─────────────────────────────────────────────────────────────────
function loop() {
  if (!isRunning) return;
  animFrame = requestAnimationFrame(loop);

  // Sync canvas size
  if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
    canvas.width  = video.videoWidth;
    canvas.height = video.videoHeight;
  }

  // FPS counter — INI ADALAH FPS RENDER VIDEO DI CANVAS, BUKAN kecepatan AI.
  // Sebelumnya label ini ditampilkan sebagai "X FPS · YOLOv8" yang menyiratkan
  // AI berjalan secepat itu, padahal AI hanya dipanggil setiap `inferInterval`
  // ms (lihat sendFrame). Sekarang dipisah jelas: "Render" vs "AI" rate, agar
  // tidak menyesatkan (video tetap mulus walau AI di belakang lebih lambat).
  frameCount++;
  const now = performance.now();
  if (now - fpsTimer >= 1000) {
    currentFps = frameCount;
    frameCount = 0;
    fpsTimer   = now;
    const aiRate = (1000 / inferInterval).toFixed(1);
    camFps.textContent  = `Render ${currentFps} FPS \u00B7 AI ~${aiRate}/s`;
    camMeta.textContent = `YOLOv8 \u00B7 SmartWaste AI`;
  }

  // Send to server every inferInterval ms — tapi jangan kalau request sebelumnya
  // masih berjalan (mencegah request menumpuk kalau server lambat)
  if (!isInferring && now - lastInfer >= inferInterval) {
    lastInfer = now;
    sendFrame(now);
  }
}

// ── Send frame to /api/camera-frame ───────────────────────────────────────────
async function sendFrame(t0) {
  const tmp = document.createElement('canvas');
  tmp.width  = Math.min(video.videoWidth,  640);
  tmp.height = Math.min(video.videoHeight, 360);
  tmp.getContext('2d').drawImage(video, 0, 0, tmp.width, tmp.height);
  const frame = tmp.toDataURL('image/jpeg', 0.7);

  isInferring = true;
  try {
    const res = await fetch('/api/camera-frame', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        frame,
        send_w: tmp.width,
        send_h: tmp.height,
      }),
    });
    const data = await res.json();
    // Pakai data.inference_ms (waktu YOLO benar-benar memproses di server),
    // bukan `elapsed` (round-trip termasuk network) — supaya angka yang
    // ditampilkan mencerminkan kecepatan model, bukan kecepatan koneksi.
    const serverMs = typeof data.inference_ms === 'number' ? data.inference_ms : Math.round(performance.now() - t0);
    inferTime.textContent = `Waktu Inferensi (server): ${serverMs}ms`;

    // Adaptive interval: sesuaikan jeda berikutnya dengan kecepatan server yang
    // sebenarnya (data.inference_ms), bukan angka tetap 500ms. Kalau server lagi
    // lambat (mis. fallback CPU), interval otomatis melebar agar tidak menumpuk.
    if (typeof data.inference_ms === 'number') {
      inferInterval = Math.min(MAX_INTERVAL, Math.max(MIN_INTERVAL, Math.round(data.inference_ms * 0.8)));
    }

    if (data.success) {
      // Filter 1: hanya tampilkan deteksi confidence >= 62%
      let filtered = (data.detections || []).filter(d => d.confidence >= 62);

      // Filter 2: deduplikasi label yang sama — ambil yang confidence tertinggi per label
      const bestByLabel = {};
      for (const det of filtered) {
        if (!bestByLabel[det.label] || det.confidence > bestByLabel[det.label].confidence) {
          bestByLabel[det.label] = det;
        }
      }
      filtered = Object.values(bestByLabel);

      drawBoxes(filtered, tmp.width, tmp.height);
      renderDetections(filtered);
    }
  } catch (_) { /* ignore transient errors */ }
  finally {
    isInferring = false;
  }
}

// ── Draw bounding boxes ───────────────────────────────────────────────────────
function drawBoxes(detections, sendW, sendH) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (!detections || detections.length === 0) {
    objCount.textContent = '0 Objek Terdeteksi';
    return;
  }
  objCount.textContent = `${detections.length} Objek Terdeteksi`;

  const scaleX = canvas.width  / sendW;
  const scaleY = canvas.height / sendH;

  detections.forEach(det => {
    const [x1, y1, x2, y2] = det.bbox;
    const sx1 = x1 * scaleX, sy1 = y1 * scaleY;
    const sx2 = x2 * scaleX, sy2 = y2 * scaleY;
    const color = det.color || '#5ba35b';
    const label = `${det.label} ${det.confidence}%`;

    // Box
    ctx.strokeStyle = color;
    ctx.lineWidth   = 2;
    ctx.shadowColor = color;
    ctx.shadowBlur  = 8;
    ctx.strokeRect(sx1, sy1, sx2 - sx1, sy2 - sy1);
    ctx.shadowBlur  = 0;

    // Label background
    ctx.font = 'bold 13px Inter, sans-serif';
    const tw = ctx.measureText(label).width;
    ctx.fillStyle = color;
    ctx.fillRect(sx1 - 1, sy1 - 26, tw + 16, 22);

    // Label text
    ctx.fillStyle = '#ffffff';
    ctx.fillText(label, sx1 + 7, sy1 - 9);
  });
}

// ── Render detection list panel ───────────────────────────────────────────────
function renderDetections(detections) {
  if (!detections || detections.length === 0) {
    detList.innerHTML = NO_OBJECT_HTML;
    return;
  }

  detList.innerHTML = '';
  detections.forEach(det => {
    const color = det.color || '#5ba35b';
    const div = document.createElement('div');
    div.className = 'det-item';
    div.innerHTML = `
      <div class="det-item-top">
        <span class="det-item-icon" style="color:${color}">${iconFor(det.icon)}</span>
        <span class="det-item-name">${det.label}</span>
        <span class="det-item-conf" style="color:${color}">${det.confidence}%</span>
      </div>
      <div class="det-bar-track">
        <div class="det-bar-fill" style="background:${color};width:${det.confidence}%"></div>
      </div>
      <div class="det-item-action">${ICON_LIGHTBULB} ${det.action || 'Pisahkan ke tempat sampah yang sesuai'}</div>
    `;
    detList.appendChild(div);
  });
}
