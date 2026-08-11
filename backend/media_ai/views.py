# ============================================================================
# App:  media_ai
# File: views.py
# Role: POST /api/media/upload/ (image -> AI response) and
#       POST /api/media/generate/ (prompt -> generated image), matching
#       frontend/src/services/api.js -> mediaApi.generateImage().
# ============================================================================

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from . import services
from .models import GeneratedImage, ImageUpload
from .serializers import (
    GenerateImageRequestSerializer,
    GeneratedImageSerializer,
    ImageUploadRequestSerializer,
    ImageUploadSerializer,
)


class ImageUploadView(APIView):
    """Guests may upload with a lighter response profile; auth users get full analysis."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ImageUploadRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        upload = ImageUpload.objects.create(
            user=request.user if request.user.is_authenticated else None,
            image=serializer.validated_data["image"],
            source_module=serializer.validated_data.get("source_module", ""),
        )
        upload.ai_response = services.analyze_image(
            upload.image, is_authenticated=request.user.is_authenticated
        )
        upload.save(update_fields=["ai_response"])

        return Response(ImageUploadSerializer(upload).data, status=status.HTTP_201_CREATED)


class GenerateImageView(APIView):
    """Image generation is an authenticated-only feature (see README V1 scope)."""

    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "image-gen"

    def post(self, request):
        serializer = GenerateImageRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        record = GeneratedImage.objects.create(user=request.user, prompt=serializer.validated_data["prompt"])
        result = services.request_image_generation(record.prompt)

        record.status = result.get("status", "failed")
        if result.get("image_url"):
            record.image = result["image_url"]
        record.save(update_fields=["status", "image"])

        return Response(GeneratedImageSerializer(record).data, status=status.HTTP_201_CREATED)