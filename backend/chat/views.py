from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from . import services
from .models import ChatSession
from .serializers import (
    ChatSessionDetailSerializer,
    ChatSessionListSerializer,
    CrisisEscalationSerializer,
    SendMessageSerializer,
)


class ChatSessionListView(ListAPIView):
    """GET /api/modules/mental-health/sessions/ — sidenav chat history (auth only)."""

    serializer_class = ChatSessionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user, is_guest_session=False)


class ChatSessionDetailView(RetrieveDestroyAPIView):
    """GET/DELETE /api/modules/mental-health/sessions/<id>/"""

    serializer_class = ChatSessionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "session_id"

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)


class SendMessageView(APIView):
    """
    POST /api/modules/mental-health/message/
    Available to guests (AllowAny) with a lighter response profile and
    tighter throttling; authenticated users get the full profile.
    """

    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]

    def get_throttles(self):
        self.throttle_scope = "auth-chat" if self.request.user.is_authenticated else "guest-chat"
        return super().get_throttles()

    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user if request.user.is_authenticated else None
        session_id = data.get("session_id")

        # Guests may only continue a guest session; never someone else's.
        if session_id and user is None:
            try:
                existing = ChatSession.objects.get(id=session_id)
                if not existing.is_guest_session:
                    raise PermissionDenied("Log in to access this conversation.")
            except ChatSession.DoesNotExist:
                pass

        session, user_message, assistant_message, escalation = services.handle_incoming_message(
            user=user,
            session_id=session_id,
            content=data.get("content", ""),
            image=data.get("image"),
        )

        response_payload = {
            "session_id": str(session.id),
            "user_message": {
                "id": str(user_message.id),
                "content": user_message.content,
                "risk_flag": user_message.risk_flag,
            },
            "assistant_message": {
                "id": str(assistant_message.id),
                "content": assistant_message.content,
                "model_version": assistant_message.model_version,
            },
            "is_guest": user is None,
        }

        if escalation:
            response_payload["crisis_escalation"] = CrisisEscalationSerializer(escalation).data
            response_payload["crisis_resources"] = escalation.resources_shown

        return Response(response_payload, status=status.HTTP_201_CREATED)