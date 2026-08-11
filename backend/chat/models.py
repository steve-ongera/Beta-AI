import uuid

from django.conf import settings
from django.db import models


class ChatSession(models.Model):
    """
    A conversation thread. Guest sessions have user=None and are never
    persisted as visible chat history (see services.py).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="mental_health_sessions",
    )
    title = models.CharField(max_length=255, blank=True, default="New conversation")
    is_guest_session = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.title} ({self.id})"


class Message(models.Model):
    class Role(models.TextChoices):
        USER = "user", "User"
        ASSISTANT = "assistant", "Assistant"
        SYSTEM = "system", "System"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=16, choices=Role.choices)
    content = models.TextField()
    image = models.ImageField(upload_to="mental_health/uploads/%Y/%m/", null=True, blank=True)

    # Safety metadata — set by services.py after each user message is screened
    risk_flag = models.CharField(max_length=32, blank=True, default="")  # e.g. "none", "watch", "high_risk"
    model_version = models.CharField(max_length=64, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"[{self.role}] {self.content[:40]}"


class CrisisEscalation(models.Model):
    """
    Logged whenever a message is screened as high-risk, so it can be
    reviewed by a human/clinical reviewer and, where configured, trigger
    an external escalation webhook.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="escalations")
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="escalations")
    reason = models.CharField(max_length=255)
    resources_shown = models.JSONField(default=list, blank=True)
    reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]