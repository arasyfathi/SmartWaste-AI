import { useEffect, useRef, useState } from 'react';

interface StatItem {
  value: string;
  label: string;
  counter?: number;
  suffix?: string;
}

const stats: StatItem[] = [
  { value: '90.02%', label: 'AKURASI KLASIFIKASI', counter: 90.02, suffix: '%' },
  { value: 'YOLOv8', label: 'DETEKSI REAL-TIME' },
  { value: '5', label: 'KATEGORI SAMPAH', counter: 5 },
  { value: '<2s', label: 'WAKTU PREDIKSI' },
  { value: '15K+', label: 'DATASET TRAINING' },
];

function AnimatedCounter({ target, suffix = '' }: { target: number; suffix?: string }) {
  const ref = useRef<HTMLSpanElement>(null);
  const [display, setDisplay] = suffix ? '0' + suffix : '0';
  const animated = useRef(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !animated.current) {
          animated.current = true;
          const isDecimal = !Number.isInteger(target);
          const duration = 1400;
          const start = performance.now();

          function tick(now: number) {
            const p = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - p, 3);
            const val = target * eased;
            const text = isDecimal ? val.toFixed(2) : String(Math.round(val));
            setDisplay(text + suffix);
            if (p < 1) requestAnimationFrame(tick);
            else setDisplay((isDecimal ? target.toFixed(2) : String(target)) + suffix);
          }
          requestAnimationFrame(tick);
        }
      },
      { threshold: 0.5 },
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [target, suffix]);

  return <span ref={ref}>{display}</span>;
}

export function StatsBar() {
  return (
    <div className="stats-bar fade-up">
      {stats.map((stat, i) => (
        <div key={i} className="stat">
          <span className="stat-num">
            {stat.counter !== undefined ? (
              <AnimatedCounter target={stat.counter} suffix={stat.suffix} />
            ) : (
              stat.value
            )}
          </span>
          <span className="stat-label">{stat.label}</span>
          {i < stats.length - 1 && <div className="stat-divider" />}
        </div>
      ))}
    </div>
  );
}
