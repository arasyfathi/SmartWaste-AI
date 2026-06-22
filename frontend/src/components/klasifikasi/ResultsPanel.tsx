import { useEffect, useRef } from 'react';
import { getMeta } from '../../lib/constants';
import { ClassIcon, RecycleIcon } from '../../lib/icons';
import type { PredictResponse } from '../../lib/api';

type ResultState = 'empty' | 'loading' | 'content' | 'error';

interface ResultsPanelProps {
  state: ResultState;
  data: PredictResponse | null;
  errorMsg: string;
  onReset: () => void;
}

export function ResultsPanel({ state, data, errorMsg, onReset }: ResultsPanelProps) {
  return (
    <div className="panel results-panel fade-up fade-up-delay-1">
      <div className="panel-header">
        <span className="panel-dot"></span>
        HASIL ANALISIS
        <span className="status-badge">
          {state === 'loading' ? 'Memproses' : state === 'error' ? 'Error' : state === 'content' ? (
            <>
              <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" fill="currentColor" fillOpacity="0.12"/><path d="M8 12.5l2.5 2.5L16 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
              Terdeteksi
            </>
          ) : 'Menunggu'}
        </span>
      </div>

      {/* Waiting state */}
      {state === 'empty' && (
        <div className="results-state">
          <div className="empty-icon">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2"/><line x1="16.5" y1="16.5" x2="21" y2="21" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/></svg>
          </div>
          <p>Upload gambar dan klik <strong>Prediksi Sekarang</strong><br />untuk melihat hasil klasifikasi</p>
        </div>
      )}

      {/* Loading */}
      {state === 'loading' && (
        <div className="results-state">
          <div className="spinner"></div>
          <p>AI sedang menganalisis gambar...</p>
        </div>
      )}

      {/* Results */}
      {state === 'content' && data && <ResultsContent data={data} />}

      {/* Error */}
      {state === 'error' && (
        <div className="results-state">
          <div className="empty-icon">
            <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2"/><line x1="12" y1="8" x2="12" y2="13" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/><circle cx="12" cy="16.5" r="1" fill="currentColor"/></svg>
          </div>
          <p>{errorMsg}</p>
          <button className="btn-ghost btn-sm" onClick={onReset}>Coba Lagi</button>
        </div>
      )}
    </div>
  );
}

function ResultsContent({ data }: { data: PredictResponse }) {
  const { prediction, confidence, all_scores, recommendation } = data;
  const meta = getMeta(prediction);

  return (
    <div>
      <div className="result-top">
        <span className="result-icon" style={{ color: meta.color }}>
          <ClassIcon name={meta.icon} />
        </span>
        <div>
          <div className="result-label" style={{ color: meta.color }}>{prediction}</div>
          <div className="result-sublabel">Kategori hasil klasifikasi</div>
        </div>
        <div className="result-conf-big" style={{ color: meta.color }}>{confidence}%</div>
      </div>

      <div className="conf-section-label">CONFIDENCE SCORE</div>
      <div className="confidence-list">
        {Object.entries(all_scores).map(([name, pct]) => {
          const m = getMeta(name);
          return (
            <ConfidenceRow key={name} name={name} pct={pct} color={m.color} icon={m.icon} />
          );
        })}
      </div>

      <div className="rec-box">
        <div className="rec-header">REKOMENDASI PENGELOLAAN</div>
        <p className="rec-text">
          {recommendation?.tips?.length
            ? recommendation.tips.join(' ')
            : `Aksi yang direkomendasikan: ${recommendation?.action || '—'}`}
        </p>
      </div>
    </div>
  );
}

function ConfidenceRow({ name, pct, color, icon }: { name: string; pct: number; color: string; icon: string }) {
  const fillRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (fillRef.current) fillRef.current.style.width = `${pct}%`;
    }, 80);
    return () => clearTimeout(timer);
  }, [pct]);

  return (
    <div className="conf-row">
      <span className="conf-row-label">
        <span className="conf-row-dot" style={{ background: color }}></span>
        {name}
      </span>
      <div className="conf-bar-track">
        <div ref={fillRef} className="conf-bar-fill" style={{ background: color, width: '0%' }}></div>
      </div>
      <span className="conf-row-val">{pct}%</span>
    </div>
  );
}
