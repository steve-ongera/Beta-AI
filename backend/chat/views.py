# ============================================================================
# App:  chat
# File: views.py
# Role: GET /api/modules/ — lists active AI app modules for the frontend
#       (sidenav / future app switcher). Matches frontend/src/services/api.js
#       -> modulesApi.list().
# ============================================================================

from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .models import AIModule
from .serializers import AIModuleSerializer


class AIModuleListView(ListAPIView):
    serializer_class = AIModuleSerializer
    permission_classes = [permissions.AllowAny]
    queryset = AIModule.objects.filter(is_active=True)