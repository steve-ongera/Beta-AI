# ============================================================================
# App:  chat
# File: serializers.py
# ============================================================================

from rest_framework import serializers

from .models import AIModule


class AIModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModule
        fields = [
            "slug",
            "name",
            "description",
            "icon",
            "is_active",
            "requires_auth_for_full_access",
            "api_base_path",
        ]