# ============================================================================
# App:  chat
# File: urls.py
# Mounted at: /api/modules/ (see config/urls.py)
# Note: this app's own list route is "" so the full path is /api/modules/.
#       Individual modules (e.g. mentalhealth) mount their own urls.py
#       one level deeper, e.g. /api/modules/mental-health/.
# ============================================================================

from django.urls import path

from .views import AIModuleListView

app_name = "chat"

urlpatterns = [
    path("", AIModuleListView.as_view(), name="module-list"),
]