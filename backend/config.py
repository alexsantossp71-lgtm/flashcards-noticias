import os
from pathlib import Path
from typing import Literal, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

# Base paths
BASE_DIR = Path(__file__).parent.parent
GENERATED_POSTS_DIR = BASE_DIR / "generated_posts"
GENERATED_POSTS_DIR.mkdir(exist_ok=True)


# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")  # Modelo primário correto
OLLAMA_FALLBACK_MODELS = ["llama3.2:3b"]  # Apenas modelos instalados
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "60"))

# Gemini API Configuration (for text generation)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# Text generation backend: 'ollama' (local, no filters) or 'gemini' (cloud, fast but filtered)
TEXT_BACKEND = os.getenv("TEXT_BACKEND", "ollama")  # Changed to Ollama as primary


# Image Generation Configuration
IMAGE_BACKEND: Literal["comfyui", "automatic1111", "fooocus", "pollinations", "diffusers"] = os.getenv(
    "IMAGE_BACKEND", "diffusers"
).lower()

# ComfyUI
COMFYUI_URL = os.getenv("COMFYUI_URL", "http://localhost:8188")
COMFYUI_TIMEOUT = int(os.getenv("COMFYUI_TIMEOUT", "180"))

# Automatic1111
A1111_URL = os.getenv("A1111_URL", "http://localhost:7860")
A1111_TIMEOUT = int(os.getenv("A1111_TIMEOUT", "45"))

# Fooocus
FOOOCUS_URL = os.getenv("FOOOCUS_URL", "http://localhost:7865")
FOOOCUS_TIMEOUT = int(os.getenv("FOOOCUS_TIMEOUT", "45"))

# Pollinations (Fallback)
POLLINATIONS_ENABLED = os.getenv("POLLINATIONS_FALLBACK", "true").lower() == "true"

# Image Settings
IMAGE_WIDTH = int(os.getenv("IMAGE_WIDTH", "1080"))
IMAGE_HEIGHT = int(os.getenv("IMAGE_HEIGHT", "1920"))
IMAGE_FORMAT = os.getenv("IMAGE_FORMAT", "PNG")

# RSS Configuration
RSS_TIMEOUT = int(os.getenv("RSS_TIMEOUT", "10"))
RSS_MAX_ITEMS = int(os.getenv("RSS_MAX_ITEMS", "25"))

# Server Configuration
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))

# CORS Settings
CORS_ORIGINS: List[str] = os.getenv(
    "CORS_ORIGINS",
    ",".join([
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "http://localhost:3005",
        "http://localhost:3006",
        "http://localhost:3007",
        "http://localhost:3008",
        "http://localhost:3009",
        "http://localhost:3010",
        "null"  # Allow local file:// protocol for vanilla JS version
    ])
).split(",")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
