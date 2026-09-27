"""
Configuration settings for the AI Smart Waste Management System.
Centralizes paths, model thresholds, camera intervals, and server parameters.
Optimized for both local development and Vercel serverless deployment.
"""

import os
import tempfile
from pathlib import Path

# Base project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Detect if running on Vercel serverless environment
IS_VERCEL = os.getenv("VERCEL") == "1"

# Optional simple .env file loader (no external dependency required)
ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.exists():
    try:
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))
    except Exception:
        pass

# Application Metadata
APP_TITLE = "♻️ AI Smart Waste Management"
APP_SUBTITLE = "Real-Time Waste Classification Using Deep Learning"
APP_VERSION = "1.0.0"

# Server Settings
HOST = os.getenv("HOST", "0.0.0.0")  # Bind to all interfaces for Vercel
PORT = int(os.getenv("PORT") or "8000")
DEBUG = os.getenv("DEBUG", "false" if IS_VERCEL else "true").lower() in ("true", "1", "yes")

# Directory Paths
# On Vercel, use /tmp for writable storage (ephemeral, clears on restart)
if IS_VERCEL:
    DATA_DIR = Path(tempfile.gettempdir()) / "smart-waste-ai" / "data"
    MODEL_DIR = BASE_DIR / "model"
    UPLOADS_DIR = Path(tempfile.gettempdir()) / "smart-waste-ai" / "uploads"
else:
    DATA_DIR = BASE_DIR / "data"
    MODEL_DIR = BASE_DIR / "model"
    UPLOADS_DIR = BASE_DIR / "uploads"

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Ensure runtime directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Database Settings
DB_PATH = Path(os.getenv("DB_PATH", str(DATA_DIR / "waste.db")))

# Machine Learning / Deep Learning Model Settings
DEFAULT_MODEL_PATH = MODEL_DIR / "waste_classifier.keras"
ALT_PYTORCH_MODEL_PATH = MODEL_DIR / "waste_classifier.pth"
MODEL_PATH = Path(os.getenv("MODEL_PATH", str(DEFAULT_MODEL_PATH)))

# Input image dimensions expected by MobileNetV2 / standard CNNs
IMAGE_SIZE = (224, 224)

# Minimum confidence score (0.0 to 1.0) before warning about uncertain prediction
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.55"))

# Duplicate Detection Debounce Window (in seconds)
DEBOUNCE_SECONDS = float(os.getenv("DEBOUNCE_SECONDS", "5.0"))

# Default Frontend Webcam Frame Capture Interval (in milliseconds)
CAPTURE_INTERVAL_MS = int(os.getenv("CAPTURE_INTERVAL_MS", "1200"))

# Supported Waste Categories (in strict canonical order)
WASTE_CATEGORIES = [
    "Plastic",
    "Paper",
    "Metal",
    "Glass",
    "Organic",
    "General Waste",
]
