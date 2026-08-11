# ============================================================================
# App:  chat
# File: models.py
# Role: Platform-wide module registry. Each pluggable AI app (mentalhealth
#       today, others later) registers one row here so the frontend sidenav
#       and a future "app switcher" can list what's available without
#       hardcoding module names.
# ============================================================================

from django.db import models


class AIModule(models.Model):
    """One entry per pluggable AI app module (e.g. mentalhealth, nutrition)."""

    slug = models.SlugField(unique=True)          # e.g. "mental-health"
    name = models.CharField(max_length=120)         # e.g. "Mental Health"
    description = models.TextField(blank=True, default="")
    icon = models.CharField(max_length=64, blank=True, default="bi-chat-heart")  # Bootstrap Icons class
    is_active = models.BooleanField(default=True)
    requires_auth_for_full_access = models.BooleanField(default=True)
    api_base_path = models.CharField(max_length=200)  # e.g. "/api/modules/mental-health/"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name