// ── Class metadata (colors & icon keys) ──────────────────────────────────────
// Source: RECOMMENDATIONS in app.py + CLASS_META in klasifikasi.js

export const CLASS_META: Record<string, { color: string; icon: string }> = {
  Plastik: { color: '#06b6d4', icon: 'plastic' },
  Kertas: { color: '#f59e0b', icon: 'paper' },
  Kaca: { color: '#8b5cf6', icon: 'glass' },
  Logam: { color: '#10d9a0', icon: 'metal' },
  Organik: { color: '#4ade80', icon: 'organic' },
};

export function getMeta(name: string) {
  return CLASS_META[name] || { color: '#5ba35b', icon: 'recycle' };
}

// ── Recommendations per category ──────────────────────────────────────────────
export interface Recommendation {
  icon: string;
  color: string;
  tips: string[];
  action: string;
}

export const RECOMMENDATIONS: Record<string, Recommendation> = {
  Plastik: {
    icon: '♻️',
    color: '#06b6d4',
    tips: [
      'Pisahkan ke tempat sampah daur ulang plastik (biasanya berwarna kuning).',
      'Cuci dan keringkan sebelum dibuang agar tidak terkontaminasi.',
      'Jangan campur dengan sampah organik atau B3.',
      'Botol plastik PET (kode 1) bernilai tinggi di bank sampah.',
    ],
    action: 'Daur Ulang',
  },
  Kertas: {
    icon: '📄',
    color: '#f59e0b',
    tips: [
      'Kumpulkan dan ikat kertas bekas, lalu setor ke bank sampah.',
      'Hindari membasahi kertas sebelum dibuang agar tetap bernilai.',
      'Kardus bisa dilipat agar hemat tempat.',
      'Kertas yang sudah terkena minyak/makanan sebaiknya dikomposkan.',
    ],
    action: 'Daur Ulang / Kompos',
  },
  Kaca: {
    icon: '🪟',
    color: '#8b5cf6',
    tips: [
      'Bungkus pecahan kaca dengan kertas tebal sebelum dibuang.',
      'Pisahkan ke tempat sampah anorganik.',
      'Botol kaca utuh bisa disetor ke pengepul atau bank sampah.',
      'Jangan bakar kaca — berbahaya dan menghasilkan gas beracun.',
    ],
    action: 'Pisahkan Khusus',
  },
  Logam: {
    icon: '⚙️',
    color: '#10d9a0',
    tips: [
      'Setor ke pengepul logam — kaleng aluminium, besi, dan tembaga bernilai tinggi.',
      'Bersihkan dari sisa makanan/minyak sebelum disetor.',
      'Jangan buang ke tempat sampah biasa karena sulit terurai.',
      'Aerosol kosong bisa dibuang ke tempat sampah B3.',
    ],
    action: 'Jual ke Pengepul',
  },
  Organik: {
    icon: '🌿',
    color: '#4ade80',
    tips: [
      'Jadikan kompos dengan mencampurnya dengan daun kering atau tanah.',
      'Sisa makanan bisa diolah menjadi pupuk cair fermentasi (eco-enzyme).',
      'Pisahkan dari sampah anorganik agar tidak mencemari daur ulang.',
      'Gunakan komposter atau lubang resapan biopori di rumah.',
    ],
    action: 'Kompos',
  },
};

// ── Class names ──────────────────────────────────────────────────────────────
export const CLASS_NAMES = ['Kaca', 'Kertas', 'Logam', 'Organik', 'Plastik'];

// ── Allowed file types ───────────────────────────────────────────────────────
export const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
