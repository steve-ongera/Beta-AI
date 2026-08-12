# ============================================================================
# File: ai-engine/main.py
# Role: The service Django's mentalhealth/services.py and media_ai/services.py
#       call via AI_ENGINE_URL. Runs entirely on your machine — no calls to
#       OpenAI/Anthropic/etc. This is "Stage 0": pattern-matching + a small
#       local knowledge base. See TRAINING_GUIDE.md for how this evolves
#       into an actual trained model.
# Run:  uvicorn main:app --port 9000 --reload
# ============================================================================

import re
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from responder import generate_response

app = FastAPI(title="MindBridge AI Engine")


class InferRequest(BaseModel):
    prompt: str
    image_path: Optional[str] = None
    profile: str = "guest_generic"   # "full" (auth) or "guest_generic" — set by Django
    domain: str = "mental_health"
    user_display_name: Optional[str] = None  # e.g. "Steve" — see services.py change below


class InferResponse(BaseModel):
    text: str
    model_version: str


@app.post("/v1/infer", response_model=InferResponse)
def infer(payload: InferRequest):
    text, version = generate_response(
        prompt=payload.prompt,
        display_name=payload.user_display_name,
        profile=payload.profile,
    )
    return InferResponse(text=text, model_version=version)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}