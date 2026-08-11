# ============================================================================
# App:  mentalhealth
# File: services.py
# Role: Business logic — session handling, risk screening, AI engine calls,
#       crisis escalation. Kept out of views.py so it's testable/reusable
#       from Celery tasks or the admin.
# ============================================================================

import logging

import requests
from django.conf import settings

from .models import ChatSession, CrisisEscalation, Message

logger = logging.getLogger(__name__)

# Minimal, non-exhaustive watch-list — real implementation should use a
# proper classifier from the AI engine, not just keyword matching.
HIGH_RISK_KEYWORDS = [
    "kill myself", "suicide", "end my life", "want to die", "hurt myself",
]

CRISIS_RESOURCES = [
    {"name": "988 Suicide & Crisis Lifeline (US)", "contact": "call or text 988"},
    {"name": "International Association for Suicide Prevention", "contact": "https://www.iasp.info/resources/Crisis_Centres/"},
]


class GuestLimitExceeded(Exception):
    pass


def get_or_create_session(user, session_id):
    """
    Returns (session, created). Guest users (user=None) always get a
    fresh, non-persisted-as-history session unless session_id is given
    for continuity within the same browser session.
    """
    if session_id:
        try:
            session = ChatSession.objects.get(id=session_id)
            if session.user_id and session.user_id != getattr(user, "id", None):
                raise PermissionError("Session does not belong to this user.")
            return session, False
        except ChatSession.DoesNotExist:
            pass

    session = ChatSession.objects.create(
        user=user if getattr(user, "is_authenticated", False) else None,
        is_guest_session=not getattr(user, "is_authenticated", False),
    )
    return session, True


def screen_for_risk(text: str) -> str:
    """Returns 'high_risk', 'watch', or 'none'. Placeholder for a real classifier."""
    lowered = (text or "").lower()
    if any(kw in lowered for kw in HIGH_RISK_KEYWORDS):
        return "high_risk"
    return "none"


def record_crisis_escalation(message: Message, session: ChatSession, reason: str):
    escalation = CrisisEscalation.objects.create(
        message=message,
        session=session,
        reason=reason,
        resources_shown=CRISIS_RESOURCES,
    )
    if settings.CRISIS_ESCALATION_WEBHOOK:
        try:
            requests.post(
                settings.CRISIS_ESCALATION_WEBHOOK,
                json={"session_id": str(session.id), "reason": reason},
                timeout=5,
            )
        except requests.RequestException:
            logger.exception("Failed to notify crisis escalation webhook")
    return escalation


def call_ai_engine(*, prompt: str, image_path: str | None, is_authenticated: bool) -> dict:
    """
    Calls the decoupled inference service (ai-engine/). Guests are routed to
    a lighter/generic response profile; authenticated users get the full,
    personalized model path.
    """
    payload = {
        "prompt": prompt,
        "image_path": image_path,
        "profile": "full" if is_authenticated else "guest_generic",
        "domain": "mental_health",
    }
    try:
        response = requests.post(
            f"{settings.AI_ENGINE_URL}/v1/infer",
            json=payload,
            timeout=settings.AI_ENGINE_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        logger.exception("AI engine call failed")
        return {
            "text": "I'm having trouble reaching the assistant right now. Please try again shortly.",
            "model_version": "unavailable",
        }


def handle_incoming_message(*, user, session_id, content, image=None):
    """
    Orchestrates one full turn: get/create session, screen risk, store the
    user message, call the model, store the assistant reply.
    Returns (session, user_message, assistant_message, crisis_escalation_or_None).
    """
    session, _ = get_or_create_session(user, session_id)

    risk = screen_for_risk(content)

    user_message = Message.objects.create(
        session=session,
        role=Message.Role.USER,
        content=content,
        image=image,
        risk_flag=risk,
    )

    escalation = None
    if risk == "high_risk":
        escalation = record_crisis_escalation(user_message, session, reason="keyword_match")
        assistant_text = (
            "I'm really glad you reached out. I want to make sure you're safe right now — "
            "please consider contacting a crisis line or someone you trust immediately. "
            "You don't have to go through this alone."
        )
        model_version = "safety_layer_v1"
    else:
        ai_response = call_ai_engine(
            prompt=content,
            image_path=image.name if image else None,
            is_authenticated=getattr(user, "is_authenticated", False),
        )
        assistant_text = ai_response.get("text", "")
        model_version = ai_response.get("model_version", "")

    assistant_message = Message.objects.create(
        session=session,
        role=Message.Role.ASSISTANT,
        content=assistant_text,
        risk_flag=risk,
        model_version=model_version,
    )

    if session.title == "New conversation" and content:
        session.title = content[:60]
    session.save(update_fields=["title", "updated_at"])

    return session, user_message, assistant_message, escalation