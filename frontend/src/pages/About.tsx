export function AboutPage() {
  return (
    <>
      <section className="page-hero">
        <div className="orb orb-1" style={{ top: '-180px', left: '-80px', opacity: 0.3 }}></div>
        <div className="orb orb-2" style={{ top: '-100px', right: '5%', opacity: 0.35 }}></div>
        <h1 className="page-title">Tentang <span className="accent">SmartWaste AI</span></h1>
        <p className="page-sub">Proyek kecerdasan buatan untuk mendukung pengelolaan sampah yang lebih baik di Indonesia</p>
        <div className="divider-line"></div>
      </section>

      <div className="about-grid">
        {/* Tujuan Proyek */}
        <div className="panel about-card fade-up">
          <div className="panel-header"><span className="panel-dot"></span>TUJUAN PROYEK</div>
          <p className="about-text">
            SmartWaste AI hadir untuk membantu masyarakat memilah sampah secara tepat menggunakan teknologi
            Computer Vision dan Deep Learning. Dengan mendeteksi kategori sampah secara otomatis, kami berharap dapat
            meningkatkan kesadaran lingkungan dan mendukung program daur ulang yang lebih efektif di Indonesia.
          </p>
        </div>

        {/* Teknologi */}
        <div className="panel about-card fade-up fade-up-delay-1">
          <div className="panel-header"><span className="panel-dot"></span>TEKNOLOGI</div>
          <div className="tech-table">
            {[
              { name: 'Python 3.11', role: 'Bahasa Pemrograman Utama' },
              { name: 'TensorFlow / Keras', role: 'Deep Learning Framework' },
              { name: 'YOLOv8 (Ultralytics)', role: 'Object Detection Real-time' },
              { name: 'OpenCV', role: 'Computer Vision Processing' },
              { name: 'Flask', role: 'Backend Web Server' },
              { name: 'HTML / CSS / JS', role: 'Frontend Interface' },
            ].map((tech) => (
              <div key={tech.name} className="tech-row">
                <span className="tech-name"><span className="tech-dot"></span>{tech.name}</span>
                <span className="tech-role">{tech.role}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Dataset */}
        <div className="panel about-card fade-up fade-up-delay-2">
          <div className="panel-header"><span className="panel-dot"></span>DATASET</div>
          <div className="ds-card">
            <div className="ds-title">Dataset Klasifikasi Sampah (Kaggle)</div>
            <div className="ds-meta">~15.870 gambar berlabel &middot; MobileNetV2 Classification</div>
          </div>
          <div className="ds-card">
            <div className="ds-title">GARBAGE CLASSIFICATION 3 (Roboflow)</div>
            <div className="ds-meta">YOLOv8 Format &middot; 6 Kelas Asli &rarr; Remap 5 Kelas &middot; Detection Real-time</div>
          </div>
          <div className="chips-wrap" style={{ padding: '0 20px 20px' }}>
            {[
              { name: 'Organik', color: '#22c55e' },
              { name: 'Kaca', color: '#06b6d4' },
              { name: 'Logam', color: '#f59e0b' },
              { name: 'Kertas', color: '#8b5cf6' },
              { name: 'Plastik', color: '#3b82f6' },
            ].map((cat) => (
              <span key={cat.name} className="chip">
                <span className="chip-dot" style={{ '--c': cat.color } as React.CSSProperties}></span>
                {' '}{cat.name}
              </span>
            ))}
          </div>
        </div>

        {/* Model AI */}
        <div className="panel about-card fade-up fade-up-delay-3">
          <div className="panel-header"><span className="panel-dot"></span>MODEL AI</div>
          <div className="model-grid">
            {[
              { val: 'MobileNetV2', key: 'KLASIFIKASI' },
              { val: 'YOLOv8m', key: 'DETEKSI RT' },
              { val: 'Auto-Resize', key: 'PRE-PROCESSING' },
              { val: 'Optimized for Speed', key: 'REAL-TIME PROCESS' },
              { val: 'Edge-Ready Design', key: 'EDGE-OPTIMIZED' },
              { val: '5 Object Classes', key: 'CLASSIFICATION OUT' },
            ].map((item) => (
              <div key={item.key} className="model-box">
                <div className="model-val">{item.val}</div>
                <div className="model-key">{item.key}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Team */}
      <section className="team-section fade-up">
        <div className="team-eyebrow">TIM PENGEMBANG</div>
        <h2 className="team-title">Mahasiswa Telkom University</h2>
        <div className="team-grid">
          {[
            { photo: '/images/ghalib.jpeg', name: 'Ghalib Hafuza', nim: '10012400211', role: 'Train Model' },
            { photo: '/images/fathi.jpeg', name: 'Fathi Arasy', nim: '101022400103', role: 'Frontend & Backend Dev' },
            { photo: '/images/adel.jpeg', name: 'Adelia Afriliani', nim: '101052300002', role: 'Web, UI/UX Design' },
          ].map((member) => (
            <div key={member.name} className="team-card">
              <div className="avatar-photo-wrap">
                <img
                  src={member.photo}
                  alt={member.name}
                  className="avatar-photo"
                />
              </div>
              <div className="member-name">{member.name}</div>
              <div className="member-nim">{member.nim}</div>
              <span className="role-badge">{member.role}</span>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
