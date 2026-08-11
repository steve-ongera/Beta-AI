# ============================================================================
# App:  users
# File: serializers.py
# Role: User profile serialization + Google token exchange input.
# ============================================================================

from rest_framework import serializers

from .models import User, UserPreferences


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ["theme", "default_module", "marketing_opt_in"]


class UserSerializer(serializers.ModelSerializer):
    preferences = UserPreferencesSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_email_verified", "date_joined", "preferences"]
        read_only_fields = ["id", "is_email_verified", "date_joined"]


class GoogleExchangeSerializer(serializers.Serializer):
    """Input for POST /api/auth/google/ — exchanges a Google ID token for our JWTs."""

    access_token = serializers.CharField()