import { useState, useRef, useCallback, useEffect } from 'react';
import { sendCameraFrame, type Detection } from '../lib/api';

const MIN_INTERVAL = 100;
const MAX_INTERVAL = 2000;

interface CameraState {
  isRunning: boolean;
  fps: number;
  aiRate: string;
  objectCount: number;
  inferenceMs: number | null;
  detections: Detection[];
}

export function useCamera() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [state, setState] = useState<CameraState>({
    isRunning: false,
    fps: 0,
    aiRate: '',
    objectCount: 0,
    inferenceMs: null,
    detections: [],
  });

  const streamRef = useRef<MediaStream | null>(null);
  const animFrameRef = useRef<number>(0);
  const isRunningRef = useRef(false);
  const facingModeRef = useRef<'environment' | 'user'>('environment');
  const lastInferRef = useRef(0);
  const inferIntervalRef = useRef(500);
  const isInferringRef = useRef(false);
  const frameCountRef = useRef(0);
  const fpsTimerRef = useRef(0);
  const currentFpsRef = useRef(0);

  const drawBoxes = useCallback((detections: Detection[], sendW: number, sendH: number) => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    if (!canvas || !video) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!detections.length) {
      setState((s) => ({ ...s, objectCount: 0 }));
      return;
    }
    setState((s) => ({ ...s, objectCount: detections.length }));

    const scaleX = canvas.width / sendW;
    const scaleY = canvas.height / sendH;

    detections.forEach((det) => {
      const [x1, y1, x2, y2] = det.bbox;
      const sx1 = x1 * scaleX, sy1 = y1 * scaleY;
      const sx2 = x2 * scaleX, sy2 = y2 * scaleY;
      const color = det.color || '#5ba35b';
      const label = `${det.label} ${det.confidence}%`;

      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.shadowColor = color;
      ctx.shadowBlur = 8;
      ctx.strokeRect(sx1, sy1, sx2 - sx1, sy2 - sy1);
      ctx.shadowBlur = 0;

      ctx.font = 'bold 13px Inter, sans-serif';
      const tw = ctx.measureText(label).width;
      ctx.fillStyle = color;
      ctx.fillRect(sx1 - 1, sy1 - 26, tw + 16, 22);
      ctx.fillStyle = '#ffffff';
      ctx.fillText(label, sx1 + 7, sy1 - 9);
    });
  }, []);

  const processFrame = useCallback(async (t0: number) => {
    const video = videoRef.current;
    if (!video) return;

    const tmp = document.createElement('canvas');
    tmp.width = Math.min(video.videoWidth, 640);
    tmp.height = Math.min(video.videoHeight, 360);
    tmp.getContext('2d')!.drawImage(video, 0, 0, tmp.width, tmp.height);
    const frame = tmp.toDataURL('image/jpeg', 0.7);

    isInferringRef.current = true;
    try {
      const data = await sendCameraFrame(frame, tmp.width, tmp.height);
      const serverMs = typeof data.inference_ms === 'number' ? data.inference_ms : Math.round(performance.now() - t0);

      if (typeof data.inference_ms === 'number') {
        inferIntervalRef.current = Math.min(MAX_INTERVAL, Math.max(MIN_INTERVAL, Math.round(data.inference_ms * 0.8)));
      }

      if (data.success) {
        let filtered = (data.detections || []).filter((d) => d.confidence >= 62);
        const bestByLabel: Record<string, Detection> = {};
        for (const det of filtered) {
          if (!bestByLabel[det.label] || det.confidence > bestByLabel[det.label].confidence) {
            bestByLabel[det.label] = det;
          }
        }
        filtered = Object.values(bestByLabel);
        drawBoxes(filtered, tmp.width, tmp.height);
        setState((s) => ({
          ...s,
          inferenceMs: serverMs,
          detections: filtered,
          aiRate: (1000 / inferIntervalRef.current).toFixed(1),
        }));
      }
    } catch {
      /* ignore transient errors */
    } finally {
      isInferringRef.current = false;
    }
  }, [drawBoxes]);

  const loop = useCallback(() => {
    if (!isRunningRef.current) return;
    animFrameRef.current = requestAnimationFrame(loop);

    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
    }

    frameCountRef.current++;
    const now = performance.now();
    if (now - fpsTimerRef.current >= 1000) {
      currentFpsRef.current = frameCountRef.current;
      frameCountRef.current = 0;
      fpsTimerRef.current = now;
      setState((s) => ({
        ...s,
        fps: currentFpsRef.current,
        aiRate: (1000 / inferIntervalRef.current).toFixed(1),
      }));
    }

    if (!isInferringRef.current && now - lastInferRef.current >= inferIntervalRef.current) {
      lastInferRef.current = now;
      processFrame(now);
    }
  }, [processFrame]);

  const startCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: facingModeRef.current, width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false,
      });
      streamRef.current = stream;
      const video = videoRef.current;
      if (video) {
        video.srcObject = stream;
        await video.play();
      }

      isRunningRef.current = true;
      fpsTimerRef.current = performance.now();
      setState((s) => ({ ...s, isRunning: true, detections: [], objectCount: 0 }));
      loop();
    } catch (err: any) {
      alert('Tidak bisa mengakses kamera: ' + (err?.message || 'Unknown error'));
    }
  }, [loop]);

  const stopCamera = useCallback(() => {
    isRunningRef.current = false;
    if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
    const video = videoRef.current;
    if (video) video.srcObject = null;
    const canvas = canvasRef.current;
    if (canvas) canvas.getContext('2d')?.clearRect(0, 0, canvas.width, canvas.height);

    setState((s) => ({
      ...s,
      isRunning: false,
      fps: 0,
      aiRate: '',
      objectCount: 0,
      inferenceMs: null,
      detections: [],
    }));
  }, []);

  const flipCamera = useCallback(async () => {
    facingModeRef.current = facingModeRef.current === 'environment' ? 'user' : 'environment';
    stopCamera();
    await startCamera();
  }, [stopCamera, startCamera]);

  const takeScreenshot = useCallback(() => {
    const video = videoRef.current;
    if (!video) return;
    const tmpCanvas = document.createElement('canvas');
    tmpCanvas.width = video.videoWidth;
    tmpCanvas.height = video.videoHeight;
    tmpCanvas.getContext('2d')!.drawImage(video, 0, 0);
    const link = document.createElement('a');
    link.download = `smartwaste_${Date.now()}.jpg`;
    link.href = tmpCanvas.toDataURL('image/jpeg', 0.9);
    link.click();
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      isRunningRef.current = false;
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop());
      }
    };
  }, []);

  return {
    videoRef,
    canvasRef,
    ...state,
    startCamera,
    stopCamera,
    flipCamera,
    takeScreenshot,
  };
}
