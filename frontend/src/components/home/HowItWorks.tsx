import { Fragment, useEffect, useRef } from 'react';

interface Step {
  num: string;
  icon: React.ReactNode;
  title: string;
  desc: string;
}

const steps: Step[] = [
  {
    num: '01',
    icon: <svg viewBox="0 0 24 24" fill="none"><path d="M12 16V4M12 4l-4 4M12 4l4 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>,
    title: 'Upload Gambar',
    desc: 'Pilih foto sampah dari perangkatmu',
  },
  {
    num: '02',
    icon: <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/></svg>,
    title: 'AI Analisis',
    desc: 'Model deep learning memproses gambar',
  },
  {
    num: '03',
    icon: <svg viewBox="0 0 24 24" fill="none"><path d="M8 12.5l2.5 2.5L16 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2"/></svg>,
    title: 'Prediksi',
    desc: 'Kategori sampah teridentifikasi',
  },
  {
    num: '04',
    icon: <svg viewBox="0 0 24 24" fill="none"><path d="M12 2l1.5 4.5L18 8l-4.5 1.5L12 14l-1.5-4.5L6 8l4.5-1.5L12 2z" fill="currentColor"/><path d="M19 14l.75 2.25L22 17l-2.25.75L19 20l-.75-2.25L16 17l2.25-.75L19 14z" fill="currentColor" opacity="0.6"/></svg>,
    title: 'Rekomendasi',
    desc: 'Dapatkan saran pengelolaan tepat',
  },
];

export function HowItWorks() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const cards = container.querySelectorAll<HTMLElement>('.step-card-3d-inner');
    const supportsHover = window.matchMedia('(hover: hover)').matches;

    if (supportsHover) {
      const maxTilt = 10;
      const handlers = Array.from(cards).map((card) => {
        const onMove = (e: MouseEvent) => {
          const rect = card.getBoundingClientRect();
          const px = (e.clientX - rect.left) / rect.width;
          const py = (e.clientY - rect.top) / rect.height;
          const rotY = (px - 0.5) * maxTilt * 2;
          const rotX = (0.5 - py) * maxTilt * 2;
          card.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg) translateZ(6px)`;
          card.style.setProperty('--mx', `${px * 100}%`);
          card.style.setProperty('--my', `${py * 100}%`);
        };
        const onLeave = () => {
          card.style.transform = 'rotateX(0deg) rotateY(0deg) translateZ(0)';
        };
        card.addEventListener('mousemove', onMove);
        card.addEventListener('mouseleave', onLeave);
        return () => {
          card.removeEventListener('mousemove', onMove);
          card.removeEventListener('mouseleave', onLeave);
        };
      });

      return () => handlers.forEach((cleanup) => cleanup());
    }
  }, []);

  return (
    <div ref={containerRef} className="steps-wrap-3d">
      {steps.map((step, i) => (
        // Fragment dengan key agar connector & card langsung jadi flex children
        // dari .steps-wrap-3d — tanpa div wrapper yang memutus flex alignment.
        <Fragment key={step.num}>
          {i > 0 && (
            <div className="step-connector-3d">
              <span></span><span></span><span></span>
            </div>
          )}
          <div className="step-card-3d" data-step={step.num}>
            <div className="step-card-3d-inner">
              <div className="step-3d-glow"></div>
              <div className="step-icon-3d">
                <div className="step-icon-3d-face">{step.icon}</div>
              </div>
              <div className="step-num-3d">{step.num}</div>
              <strong>{step.title}</strong>
              <p>{step.desc}</p>
            </div>
          </div>
        </Fragment>
      ))}
    </div>
  );
}
