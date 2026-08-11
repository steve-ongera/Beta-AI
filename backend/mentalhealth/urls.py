# ============================================================================
# App:  mentalhealth
# File: urls.py
# Mounted at: /api/modules/mental-health/ (see config/urls.py)
# ============================================================================

from django.urls import path

from .views import ChatSessionDetailView, ChatSessionListView, SendMessageView

app_name = "mentalhealth"

urlpatterns = [
    path("sessions/", ChatSessionListView.as_view(), name="session-list"),
    path("sessions/<uuid:session_id>/", ChatSessionDetailView.as_view(), name="session-detail"),
    path("message/", SendMessageView.as_view(), name="send-message"),
]