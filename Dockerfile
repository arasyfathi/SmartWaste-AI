# ─────────────────────────────────────────────────────────────────────────────
# Dockerfile — Hugging Face Spaces (Docker SDK)
# SmartWaste AI Backend — CPU-only deployment
#
# HF Spaces automatically builds and runs this container.
# App must listen on port 7860 (HF default).
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.11-slim

# System deps (OpenCV needs libgl, libglib; Pillow needs libjpeg, zlib)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps (CPU-only torch via --extra-index-url in requirements)
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend code (app.py, drive_storage.py, auth_setup.py)
COPY backend/*.py ./

# Copy ML models into container
# These must exist in the repo — use `git lfs` or force-push them
COPY model/ ./model/

# (Optional) Google Drive token — omit if not using Drive integration
# COPY backend/token.json ./token.json

# HF Spaces port
ENV PORT=7860
EXPOSE 7860

# Single worker (ML models load once), threading for concurrent requests
# Timeout 120s to allow model warmup on cold start
CMD ["gunicorn", "app:app", \
     "--bind", "0.0.0.0:7860", \
     "--workers", "1", \
     "--worker-class", "gthread", \
     "--threads", "4", \
     "--timeout", "120"]
