# ============================================================================
# App:  media_ai
# File: urls.py
# Mounted at: /api/media/ (see config/urls.py)
# ============================================================================

from django.urls import path

from .views import GenerateImageView, ImageUploadView

app_name = "media_ai"

urlpatterns = [
    path("upload/", ImageUploadView.as_view(), name="upload"),
    path("generate/", GenerateImageView.as_view(), name="generate"),
]