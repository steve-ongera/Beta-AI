# ============================================================================
# App:  users
# File: models.py
# Role: Custom user model (so we can extend it later — e.g. locale, consent
#       flags) plus a lightweight profile for platform-wide preferences.
# ============================================================================

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extends Django's default user. Kept close to stock on purpose — auth
    stays boring and battle-tested; anything module-specific (e.g. mental
    health intake data) belongs in that module's own app, not here.
    """

    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    signed_up_via_google = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


class UserPreferences(models.Model):
    """Platform-wide preferences, shared across all AI app modules."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    theme = models.CharField(max_length=16, default="light", choices=[("light", "Light"), ("dark", "Dark")])
    default_module = models.CharField(max_length=64, default="mentalhealth")
    marketing_opt_in = models.BooleanField(default=False)

    def __str__(self):
        return f"Preferences for {self.user.username}"