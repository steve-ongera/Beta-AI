# ============================================================================
# App:  media_ai
# File: models.py
# Role: Tracks image uploads (for AI analysis) and image generation requests,
#       independent of any one module — mentalhealth's message-attached
#       images reuse this app's services, but the log lives here so it's
#       reusable by future modules too.
# ============================================================================

import uuid

from django.conf import settings
from django.db import models


class ImageUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="image_uploads"
    )
    image = models.ImageField(upload_to="media_ai/uploads/%Y/%m/")
    ai_response = models.TextField(blank=True, default="")
    source_module = models.CharField(max_length=64, blank=True, default="")  # e.g. "mentalhealth"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class GeneratedImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="generated_images")
    prompt = models.TextField()
    image = models.ImageField(upload_to="media_ai/generated/%Y/%m/", null=True, blank=True)
    status = models.CharField(
        max_length=16,
        choices=[("pending", "Pending"), ("complete", "Complete"), ("failed", "Failed")],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]