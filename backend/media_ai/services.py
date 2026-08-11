# ============================================================================
# App:  media_ai
# File: services.py
# Role: Calls out to the decoupled inference/image-gen services. Kept
#       separate from views.py for testability and reuse across modules.
# ============================================================================

import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def analyze_image(image_file, *, is_authenticated: bool) -> str:
    """Sends an uploaded image to the AI engine's vision endpoint, returns text."""
    try:
        response = requests.post(
            f"{settings.AI_ENGINE_URL}/v1/vision",
            files={"image": image_file},
            data={"profile": "full" if is_authenticated else "guest_generic"},
            timeout=settings.AI_ENGINE_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json().get("text", "")
    except requests.RequestException:
        logger.exception("Image analysis call failed")
        return "I couldn't process that image right now — please try again shortly."


def request_image_generation(prompt: str) -> dict:
    """Calls the image generation service. Returns {"status", "image_url"}."""
    try:
        response = requests.post(
            f"{settings.IMAGE_GEN_SERVICE_URL}/v1/generate",
            json={"prompt": prompt},
            timeout=settings.AI_ENGINE_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        logger.exception("Image generation call failed")
        return {"status": "failed", "image_url": None}