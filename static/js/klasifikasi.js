// ── SmartWaste AI — klasifikasi.js ────────────────────────────────────────────

// Warna & ikon per kategori (5 kelas MobileNetV2)
const CLASS_META = {
  'Plastik': { color: '#3b82f6', icon: 'plastic' },
  'Kertas':  { color: '#8b5cf6', icon: 'paper' },
  'Kaca':    { color: '#06b6d4', icon: 'glass' },
  'Logam':   { color: '#f59e0b', icon: 'metal' },
  'Organik': { color: '#22c55e', icon: 'organic' },
};

const ICONS = {
  plastic: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="8" y="3" width="8" height="3" rx="1" fill="currentColor" opacity="0.5"/><path d="M9 6v2.5L7 11v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-9l-2-2.5V6" stroke="currentColor" stroke-width="2" stroke-linejoin="round" fill="currentColor" fill-opacity="0.12"/><line x1="7.5" y1="14" x2="16.5" y2="14" stroke="currentColor" stroke-width="2"/></svg>`,
  paper: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M14 2v6h6" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><line x1="8" y1="13" x2="16" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="8" y1="17" x2="13" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`,
  glass: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7 3h10l-1.2 13.5a3.5 3.5 0 0 1-3.49 3.2h-.62a3.5 3.5 0 0 1-3.49-3.2L7 3z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" fill="currentColor" fill-opacity="0.1"/><line x1="7.6" y1="9" x2="16.4" y2="9" stroke="currentColor" stroke-width="2"/></svg>`,
  metal: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>`,
  organic: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" fill="currentColor" opacity="0.18"/><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 11 13 11 11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  cardboard: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>`,
  recycle: `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M11 19h8.203a1.83 1.83 0 0 0 1.556-.89 1.784 1.784 0 0 0 0-1.775l-1.226-2.12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="m14 16-3 3 3 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8.293 13.596 7.196 9.5 3.1 10.598" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="m9.344 5.811 1.093-1.892A1.83 1.83 0 0 1 11.985 3a1.784 1.784 0 0 1 1.546.888l3.943 6.843" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="m13.378 9.633 4.096 1.098 1.097-4.096" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
};

function getMeta(name) {
  return CLASS_META[name] || { color: '#5ba35b', icon: 'recycle' };
}

const dropzone      = document.getElementById('dropzone');
const fileInput     = document.getElementById('file-input');
const previewImg    = document.getElementById('preview-img');
const previewPh     = document.getElementById('preview-placeholder');
const predictBtn    = document.getElementById('predict-btn');
const statusBadge   = document.getElementById('status-badge');

const stateEmpty    = document.getElementById('results-empty');
const stateLoading  = document.getElementById('results-loading');
const stateContent  = document.getElementById('results-content');
const stateError    = document.getElementById('results-error');

let selectedFile = null;

// ── File selection ─────────────────────────────────────────────────────────────
dropzone.addEventListener('click', () => fileInput.click());
dropzone.addEventListener('keydown', e => {
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fileInput.click(); }
});
dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('drag-over'); });
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('drag-over'));
dropzone.addEventListener('drop', e => {
  e.preventDefault();
  dropzone.classList.remove('drag-over');
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', e => {
  if (e.target.files[0]) handleFile(e.target.files[0]);
});

function handleFile(file) {
  const allowed = ['image/jpeg', 'image/png', 'image/webp'];
  if (!allowed.includes(file.type)) { alert('Format tidak didukung. Gunakan JPG, PNG, atau WEBP.'); return; }
  if (file.size > 10 * 1024 * 1024) { alert('Ukuran file maksimal 10MB.'); return; }

  selectedFile = file;
  const reader = new FileReader();
  reader.onload = e => {
    previewImg.src = e.target.result;
    previewImg.style.display = 'block';
    previewPh.style.display  = 'none';
  };
  reader.readAsDataURL(file);
  predictBtn.disabled = false;
  showState('empty');
}

// ── Predict ────────────────────────────────────────────────────────────────────
predictBtn.addEventListener('click', async () => {
  if (!selectedFile) return;
  showState('loading');

  const formData = new FormData();
  formData.append('image', selectedFile);

  try {
    const res  = await fetch('/api/predict', { method: 'POST', body: formData });
    const data = await res.json();
    if (data.success) renderResults(data);
    else showState('error', data.error || 'Prediksi gagal.');
  } catch (err) {
    showState('error', 'Tidak bisa terhubung ke server.');
  }
});

// ── Render results ─────────────────────────────────────────────────────────────
function renderResults(data) {
  const { prediction, confidence, all_scores, recommendation } = data;
  const meta = getMeta(prediction);

  document.getElementById('result-icon').innerHTML       = ICONS[meta.icon] || ICONS.recycle;
  document.getElementById('result-icon').style.color     = meta.color;
  document.getElementById('result-label').textContent    = prediction;
  document.getElementById('result-label').style.color    = meta.color;
  document.getElementById('result-conf-big').textContent = confidence + '%';
  document.getElementById('result-conf-big').style.color = meta.color;

  // Confidence list (replaces single bar + all-bars from old layout)
  const list = document.getElementById('confidence-list');
  list.innerHTML = '';
  Object.entries(all_scores).forEach(([name, pct]) => {
    const m = getMeta(name);
    const row = document.createElement('div');
    row.className = 'conf-row';
    row.innerHTML = `
      <span class="conf-row-label"><span class="conf-row-dot" style="background:${m.color}"></span>${name}</span>
      <div class="conf-bar-track"><div class="conf-bar-fill" style="background:${m.color};width:0%"></div></div>
      <span class="conf-row-val">${pct}%</span>`;
    list.appendChild(row);
    setTimeout(() => { row.querySelector('.conf-bar-fill').style.width = pct + '%'; }, 80);
  });

  document.getElementById('rec-text').textContent =
    (recommendation && recommendation.tips && recommendation.tips.length)
      ? recommendation.tips.join(' ')
      : `Aksi yang direkomendasikan: ${recommendation && recommendation.action ? recommendation.action : '—'}`;

  statusBadge.innerHTML = `
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="9" fill="currentColor" fill-opacity="0.12"/><path d="M8 12.5l2.5 2.5L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    Terdeteksi`;
  statusBadge.className = 'status-badge';
  showState('content');
}

// ── State manager ──────────────────────────────────────────────────────────────
function showState(state, errMsg = '') {
  stateEmpty.style.display   = state === 'empty'   ? 'flex'  : 'none';
  stateLoading.style.display = state === 'loading' ? 'flex'  : 'none';
  stateContent.style.display = state === 'content' ? 'block' : 'none';
  stateError.style.display   = state === 'error'   ? 'flex'  : 'none';

  if (state === 'loading') {
    predictBtn.disabled = true;
    statusBadge.textContent = 'Memproses';
    statusBadge.className   = 'status-badge';
  }
  if (state === 'error') {
    document.getElementById('error-msg').textContent = errMsg;
    statusBadge.textContent = 'Error';
    statusBadge.className   = 'status-badge live';
    predictBtn.disabled = false;
  }
  if (state === 'empty') {
    statusBadge.textContent = 'Menunggu';
    statusBadge.className   = 'status-badge';
  }
}

window.resetUI = function () {
  showState('empty');
  predictBtn.disabled = !selectedFile;
};
