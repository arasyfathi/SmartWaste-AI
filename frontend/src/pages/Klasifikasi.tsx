import { useState, useCallback } from 'react';
import { UploadPanel } from '../components/klasifikasi/UploadPanel';
import { ResultsPanel } from '../components/klasifikasi/ResultsPanel';
import { TipsRow } from '../components/klasifikasi/TipsRow';
import { predictImage, type PredictResponse } from '../lib/api';

type ResultState = 'empty' | 'loading' | 'content' | 'error';

export function Klasifikasi() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [resultState, setResultState] = useState<ResultState>('empty');
  const [resultData, setResultData] = useState<PredictResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState('');

  const handlePredict = useCallback(async () => {
    if (!selectedFile) return;
    setResultState('loading');

    try {
      const data = await predictImage(selectedFile);
      if (data.success) {
        setResultData(data);
        setResultState('content');
      } else {
        setErrorMsg(data.error || 'Prediksi gagal.');
        setResultState('error');
      }
    } catch {
      setErrorMsg('Tidak bisa terhubung ke server.');
      setResultState('error');
    }
  }, [selectedFile]);

  const handleReset = useCallback(() => {
    setResultState('empty');
    setErrorMsg('');
  }, []);

  return (
    <>
      <section className="page-hero">
        <div className="orb orb-1" style={{ top: '-160px', right: '-100px', opacity: 0.4 }}></div>
        <h1 className="page-title">Klasifikasi <span className="accent">Sampah</span></h1>
        <p className="page-sub">Upload gambar sampah dan biarkan AI menganalisisnya dengan cepat &amp; akurat</p>
        <div className="divider-line"></div>
      </section>

      <div className="klasifikasi-layout">
        <UploadPanel
          onFileSelect={setSelectedFile}
          onPredict={handlePredict}
          selectedFile={selectedFile}
          isPredicting={resultState === 'loading'}
        />
        <ResultsPanel
          state={resultState}
          data={resultData}
          errorMsg={errorMsg}
          onReset={handleReset}
        />
      </div>

      <TipsRow />
    </>
  );
}
