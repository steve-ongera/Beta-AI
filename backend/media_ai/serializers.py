# ============================================================================
# App:  media_ai
# File: serializers.py
# ============================================================================

from rest_framework import serializers

from .models import GeneratedImage, ImageUpload


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ["id", "image", "ai_response", "source_module", "created_at"]
        read_only_fields = ["id", "ai_response", "created_at"]


class ImageUploadRequestSerializer(serializers.Serializer):
    image = serializers.ImageField()
    source_module = serializers.CharField(required=False, default="")


class GenerateImageRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=2000)


class GeneratedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedImage
        fields = ["id", "prompt", "image", "status", "created_at"]
        read_only_fields = fields