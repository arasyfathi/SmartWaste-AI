import { Link } from 'react-router-dom';
import { ScrollReveal } from '../components/ui/ScrollReveal';
import { StatsBar } from '../components/home/StatsBar';
import { FeaturesGrid } from '../components/home/FeaturesGrid';
import { HowItWorks } from '../components/home/HowItWorks';
import { WasteCategories } from '../components/home/WasteCategories';

export function Home() {
  return (
    <>
      {/* Hero */}
      <section className="hero">
        <div className="hero-orbit">
          <div className="orbit-ring"></div>
          <div className="orbit-core">
            <svg viewBox="0 0 24 24" fill="none"><path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M11 19h8.203a1.83 1.83 0 0 0 1.556-.89 1.784 1.784 0 0 0 0-1.775l-1.226-2.12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="m14 16-3 3 3 3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M8.293 13.596 7.196 9.5 3.1 10.598" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="m9.344 5.811 1.093-1.892A1.83 1.83 0 0 1 11.985 3a1.784 1.784 0 0 1 1.546.888l3.943 6.843" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="m13.378 9.633 4.096 1.098 1.097-4.096" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
          </div>
          <div className="orbit-satellites">
            <div className="orbit-chip c1" style={{ color: '#f59e0b' }} title="Logam">
              <svg viewBox="0 0 24 24" fill="none"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" fill="currentColor" fillOpacity="0.12" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/></svg>
            </div>
            <div className="orbit-chip c2" style={{ color: '#3b82f6' }} title="Plastik">
              <svg viewBox="0 0 24 24" fill="none"><rect x="8" y="3" width="8" height="3" rx="1" fill="currentColor" opacity="0.5"/><path d="M9 6v2.5L7 11v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-9l-2-2.5V6" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" fill="currentColor" fillOpacity="0.12"/><line x1="7.5" y1="14" x2="16.5" y2="14" stroke="currentColor" strokeWidth="2"/></svg>
            </div>
            <div className="orbit-chip c3" style={{ color: '#22c55e' }} title="Organik">
              <svg viewBox="0 0 24 24" fill="none"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" fill="currentColor" opacity="0.18"/><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 11 13 11 11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
            </div>
            <div className="orbit-chip c4" style={{ color: '#8b5cf6' }} title="Kertas">
              <svg viewBox="0 0 24 24" fill="none"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" fill="currentColor" fillOpacity="0.12" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/><path d="M14 2v6h6" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/><line x1="8" y1="13" x2="16" y2="13" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/><line x1="8" y1="17" x2="13" y2="17" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/></svg>
            </div>
          </div>
        </div>

        <div className="hero-content">
          <div className="badge">
            <span className="badge-dot"></span>
            <svg viewBox="0 0 24 24" fill="none"><path d="M12 2l1.5 4.5L18 8l-4.5 1.5L12 14l-1.5-4.5L6 8l4.5-1.5L12 2z" fill="currentColor"/><path d="M19 14l.75 2.25L22 17l-2.25.75L19 20l-.75-2.25L16 17l2.25-.75L19 14z" fill="currentColor" opacity="0.6"/></svg>
            AI-POWERED WASTE CLASSIFICATION
          </div>
          <h1 className="hero-title">
            Kenali Sampahmu,<br />
            <span className="accent">Jaga Bumi Kita</span>
          </h1>
          <p className="hero-sub">
            Upload foto sampah &amp; deteksi real-time dengan kamera — didukung YOLOv8 +
            MobileNetV2 akurasi tinggi untuk masa depan lingkungan yang lebih baik.
          </p>
          <div className="hero-actions">
            <Link to="/klasifikasi" className="btn-primary">
              <svg viewBox="0 0 24 24" fill="none"><path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z" fill="currentColor"/></svg>
              Mulai Klasifikasi
            </Link>
            <Link to="/camera" className="btn-secondary">
              <svg viewBox="0 0 24 24" fill="none"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/><circle cx="12" cy="13" r="3.5" fill="currentColor" opacity="0.4"/></svg>
              Coba Kamera Live
            </Link>
            <Link to="/about" className="btn-ghost">
              <svg viewBox="0 0 24 24" fill="none"><path d="M12 7c-2-1.5-4.5-2-7-2v13c2.5 0 5 .5 7 2 2-1.5 4.5-2 7-2V5c-2.5 0-5 .5-7 2z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" fill="currentColor" fillOpacity="0.08"/><line x1="12" y1="7" x2="12" y2="20" stroke="currentColor" strokeWidth="2"/></svg>
              Pelajari Lebih
            </Link>
          </div>
        </div>

        <StatsBar />
      </section>

      {/* Features */}
      <section className="section">
        <ScrollReveal>
          <div className="section-eyebrow">
            <span className="section-eyebrow-line"></span>
            FITUR UNGGULAN
          </div>
          <h2 className="section-title">Teknologi terdepan untuk<br /><span>pemilahan sampah</span></h2>
        </ScrollReveal>
        <ScrollReveal delay={1}>
          <FeaturesGrid />
        </ScrollReveal>
      </section>

      {/* How It Works */}
      <div className="section-alt">
        <section className="section">
          <ScrollReveal>
            <div className="section-eyebrow">
              <span className="section-eyebrow-line"></span>
              CARA KERJA
            </div>
            <h2 className="section-title">Empat langkah, <span>satu tujuan</span></h2>
          </ScrollReveal>
          <ScrollReveal delay={1}>
            <HowItWorks />
          </ScrollReveal>
        </section>
      </div>

      {/* Waste Categories */}
      <section className="section">
        <ScrollReveal>
          <div className="section-eyebrow">
            <span className="section-eyebrow-line"></span>
            KATEGORI SAMPAH
          </div>
          <h2 className="section-title">5 jenis sampah yang <span>dapat dideteksi</span></h2>
        </ScrollReveal>
        <ScrollReveal delay={1}>
          <WasteCategories />
        </ScrollReveal>
      </section>
    </>
  );
}
