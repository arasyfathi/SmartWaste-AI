// ── API client ───────────────────────────────────────────────────────────────

const API_BASE = import.meta.env.VITE_API_URL || '';

export interface PredictResponse {
  success: boolean;
  prediction: string;
  confidence: number;
  all_scores: Record<string, number>;
  recommendation: {
    icon: string;
    color: string;
    tips: string[];
    action: string;
  };
  model_used: string;
  error?: string;
}

export interface Detection {
  label: string;
  confidence: number;
  bbox: [number, number, number, number];
  color: string;
  icon: string;
  action: string;
}

export interface CameraFrameResponse {
  success: boolean;
  detections: Detection[];
  inference_ms: number;
  model: string;
  error?: string;
}

export interface StatusResponse {
  keras_model: boolean;
  yolo_model: boolean;
  yolo_path: string | null;
  yolo_device: string;
  classes_keras: string[];
  classes_yolo: string[];
  keras_loaded: boolean;
  yolo_loaded: boolean;
}

export async function predictImage(file: File): Promise<PredictResponse> {
  const formData = new FormData();
  formData.append('image', file);

  const res = await fetch(`${API_BASE}/api/predict`, {
    method: 'POST',
    body: formData,
  });

  return res.json();
}

export async function sendCameraFrame(
  frame: string,
  sendW: number,
  sendH: number,
): Promise<CameraFrameResponse> {
  const res = await fetch(`${API_BASE}/api/camera-frame`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ frame, send_w: sendW, send_h: sendH }),
  });

  return res.json();
}

export async function getStatus(): Promise<StatusResponse> {
  const res = await fetch(`${API_BASE}/api/status`);
  return res.json();
}
