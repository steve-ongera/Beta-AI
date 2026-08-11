from rest_framework import serializers

from ..chat.models import ChatSession, CrisisEscalation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "role",
            "content",
            "image",
            "risk_flag",
            "model_version",
            "created_at",
        ]
        read_only_fields = ["id", "risk_flag", "model_version", "created_at"]


class ChatSessionListSerializer(serializers.ModelSerializer):
    """Lightweight — used for the sidenav chat history list."""

    last_message_preview = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ["id", "title", "updated_at", "last_message_preview"]

    def get_last_message_preview(self, obj):
        last = obj.messages.order_by("-created_at").first()
        if not last:
            return ""
        return last.content[:80]


class ChatSessionDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ["id", "title", "is_guest_session", "created_at", "updated_at", "messages"]


class SendMessageSerializer(serializers.Serializer):
    """Input serializer for POST /modules/mental-health/message/"""

    session_id = serializers.UUIDField(required=False, allow_null=True)
    content = serializers.CharField(allow_blank=True, required=False, default="")
    image = serializers.ImageField(required=False, allow_null=True)

    def validate(self, attrs):
        if not attrs.get("content") and not attrs.get("image"):
            raise serializers.ValidationError("Either 'content' or 'image' is required.")
        return attrs


class CrisisEscalationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisisEscalation
        fields = ["id", "message", "session", "reason", "resources_shown", "reviewed", "created_at"]
        read_only_fields = fields