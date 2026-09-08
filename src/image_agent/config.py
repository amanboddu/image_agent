"""App configuration. Loads env vars from .env when present."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

# Replicate API token. Required. Get one at:
# https://replicate.com/account/api-tokens
REPLICATE_API_TOKEN: str | None = os.getenv("REPLICATE_API_TOKEN")

# Model to run. Override via env if you want a different one.
MODEL_ID: str = os.getenv("MODEL_ID", "google/nano-banana-2")

# UI limits for the "number of images" control.
MIN_IMAGES = 1
MAX_IMAGES = 4

# Default output image format ("png" or "jpg").
OUTPUT_FORMAT = "png"


def require_token() -> str:
    """Return the API token or raise a clear error."""
    if not REPLICATE_API_TOKEN:
        raise RuntimeError(
            "REPLICATE_API_TOKEN is not set. Copy .env.example to .env and add your token."
        )
    return REPLICATE_API_TOKEN
