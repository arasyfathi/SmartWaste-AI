const features = [
  {
    accent: '#7c3aed',
    icon: (
      <svg viewBox="0 0 24 24" fill="none"><path d="M9.5 2A2.5 2.5 0 0 0 7 4.5v.5h-.5A2.5 2.5 0 0 0 4 7.5v.879a2.5 2.5 0 0 0-1.5 2.286v1.67a2.5 2.5 0 0 0 1.5 2.286v.879a2.5 2.5 0 0 0 2.5 2.5H7v.5A2.5 2.5 0 0 0 9.5 21h.25a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1H9.5z" fill="currentColor"/><path d="M14.5 2A2.5 2.5 0 0 1 17 4.5v.5h.5A2.5 2.5 0 0 1 20 7.5v.879a2.5 2.5 0 0 1 1.5 2.286v1.67a2.5 2.5 0 0 1-1.5 2.286v.879A2.5 2.5 0 0 1 17.5 18H17v.5a2.5 2.5 0 0 1-2.5 2.5h-.25a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h.25z" fill="currentColor" opacity="0.55"/></svg>
    ),
    title: 'Deep Learning',
    desc: 'MobileNetV2 terlatih 15K+ gambar sampah untuk klasifikasi akurat & konsisten.',
    num: '01',
  },
  {
    accent: '#f59e0b',
    icon: (
      <svg viewBox="0 0 24 24" fill="none"><path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z" fill="currentColor"/></svg>
    ),
    title: 'YOLOv8 Real-time',
    desc: 'Deteksi & klasifikasi objek sampah dalam milidetik via webcam browser.',
    num: '02',
  },
  {
    accent: '#22c55e',
    icon: (
      <svg viewBox="0 0 24 24" fill="none"><path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M11 19h8.203a1.83 1.83 0 0 0 1.556-.89 1.784 1.784 0 0 0 0-1.775l-1.226-2.12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="m14 16-3 3 3 3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M8.293 13.596 7.196 9.5 3.1 10.598" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="m9.344 5.811 1.093-1.892A1.83 1.83 0 0 1 11.985 3a1.784 1.784 0 0 1 1.546.888l3.943 6.843" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="m13.378 9.633 4.096 1.098 1.097-4.096" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
    ),
    title: 'Rekomendasi Cerdas',
    desc: 'Saran pengelolaan sampah yang tepat berdasarkan kategori hasil prediksi AI.',
    num: '03',
  },
  {
    accent: '#0ea5e9',
    icon: (
      <svg viewBox="0 0 24 24" fill="none"><path d="M3 3v16a2 2 0 0 0 2 2h16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><rect x="7" y="13" width="3" height="5" rx="1" fill="currentColor"/><rect x="12" y="9" width="3" height="9" rx="1" fill="currentColor" opacity="0.6"/><rect x="17" y="5" width="3" height="13" rx="1" fill="currentColor" opacity="0.85"/></svg>
    ),
    title: 'Confidence Score',
    desc: 'Tingkat keyakinan model AI ditampilkan secara visual dan transparan.',
    num: '04',
  },
  {
    accent: '#ea580c',
    icon: (
      <svg viewBox="0 0 24 24" fill="none"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/><circle cx="12" cy="13" r="3.5" fill="currentColor" opacity="0.55"/></svg>
    ),
    title: 'Camera Detection',
    desc: 'Deteksi real-time dengan bounding box overlay langsung di UI.',
    num: '05',
  },
  {
    accent: '#db2777',
    icon: (
      <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2"/><circle cx="12" cy="12" r="5" stroke="currentColor" strokeWidth="2"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>
    ),
    title: '5 Kategori Sampah',
    desc: 'Organik, Kaca, Logam, Kertas, Plastik — terdeteksi otomatis.',
    num: '06',
  },
];

export function FeaturesGrid() {
  return (
    <div className="feature-grid">
      {features.map((f) => (
        <div key={f.num} className="feature-card" style={{ '--accent': f.accent } as React.CSSProperties}>
          <div className="fc-icon">{f.icon}</div>
          <h3>{f.title}</h3>
          <p>{f.desc}</p>
          <span className="fc-num">{f.num}</span>
        </div>
      ))}
    </div>
  );
}
