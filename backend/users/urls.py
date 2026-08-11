# ============================================================================
# App:  users
# File: urls.py
# Mounted at: /api/auth/ (see config/urls.py)
# ============================================================================

from django.urls import path

from .views import GoogleExchangeView, MeView

app_name = "users"

urlpatterns = [
    path("user/", MeView.as_view(), name="me"),
    path("google/", GoogleExchangeView.as_view(), name="google-exchange"),
]