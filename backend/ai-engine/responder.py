# ============================================================================
# File: ai-engine/responder.py
# Role: The actual response logic. Today: greeting personalization + a small
#       local FAQ retrieval, all rule-based — deliberately simple so it's
#       transparent and safe while you build up training data. This is the
#       exact function you'll swap for a real model call in Stage 2 (see
#       TRAINING_GUIDE.md) without changing main.py's API shape at all.
# ============================================================================

import re

GREETING_PATTERNS = re.compile(
    r"^\s*(hi|hello|hey|good\s?(morning|afternoon|evening)|yo|sup)\b", re.IGNORECASE
)

# Stage 0 local knowledge base — replace/extend with doctor-reviewed content.
# This is your RAG corpus in miniature: plain keyword match today, real
# embedding-based retrieval later (same data, better matching).
KNOWLEDGE_BASE = [
    {
        "keywords": ["anxious", "anxiety", "nervous", "worried"],
        "response": (
            "It sounds like you're feeling anxious. That's a really common experience, and it "
            "often shows up right before something that matters to you. Would it help to talk "
            "through what's making you feel this way?"
        ),
    },
    {
        "keywords": ["can't sleep", "insomnia", "trouble sleeping"],
        "response": (
            "Trouble sleeping can make everything else feel harder. Has this been going on for "
            "a while, or is it more of a recent thing?"
        ),
    },
    {
        "keywords": ["stressed", "overwhelmed", "too much"],
        "response": (
            "It sounds like a lot is on your plate right now. What feels like the biggest source "
            "of that right now?"
        ),
    },
]

FALLBACK_RESPONSE = (
    "I hear you. I don't have enough training data yet to respond to that specifically, but "
    "I'm listening — can you tell me more about what's going on?"
)


def generate_response(*, prompt: str, display_name: str | None, profile: str) -> tuple[str, str]:
    """
    Returns (response_text, model_version_label).
    model_version_label shows up in Message.model_version in Django — useful
    for telling seeded/rule-based responses apart from a real model later.
    """
    text = prompt.strip()

    if GREETING_PATTERNS.match(text):
        name_part = f", {display_name}" if display_name and profile == "full" else ""
        return (
            f"Hi{name_part}! I'm here and ready to listen. How are you doing today, "
            f"and how can I help?",
            "stage0_rules_v1",
        )

    lowered = text.lower()
    for entry in KNOWLEDGE_BASE:
        if any(kw in lowered for kw in entry["keywords"]):
            return entry["response"], "stage0_rules_v1"

    return FALLBACK_RESPONSE, "stage0_rules_v1"