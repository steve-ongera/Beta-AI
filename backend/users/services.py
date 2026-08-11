# ============================================================================
# App:  users
# File: services.py
# Role: Google OAuth token verification + get-or-create user logic, kept out
#       of views.py for testability.
# ============================================================================

import logging

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from .models import User, UserPreferences

logger = logging.getLogger(__name__)


class InvalidGoogleToken(Exception):
    pass


def verify_google_token(token: str) -> dict:
    """Verifies a Google ID token and returns its payload (email, name, sub)."""
    try:
        return id_token.verify_oauth2_token(token, google_requests.Request())
    except ValueError as exc:
        logger.warning("Invalid Google token: %s", exc)
        raise InvalidGoogleToken(str(exc)) from exc


def get_or_create_user_from_google(payload: dict) -> tuple[User, bool]:
    email = payload["email"]
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "username": email.split("@")[0],
            "is_email_verified": payload.get("email_verified", False),
            "signed_up_via_google": True,
        },
    )
    if created:
        UserPreferences.objects.create(user=user)
    return user, created