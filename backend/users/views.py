# ============================================================================
# App:  users
# File: views.py
# Role: /me profile endpoint + Google token exchange (issues our own JWTs).
# ============================================================================

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from . import services
from .serializers import GoogleExchangeSerializer, UserPreferencesSerializer, UserSerializer
from .models import UserPreferences


class MeView(APIView):
    """
    GET  /api/auth/user/ — current user's profile.
    PATCH /api/auth/user/ — update preferences (theme, default_module,
                             marketing_opt_in). Powers SettingsPage.jsx.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        prefs, _ = UserPreferences.objects.get_or_create(user=request.user)
        serializer = UserPreferencesSerializer(prefs, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)


class GoogleExchangeView(APIView):
    """
    POST /api/auth/google/  { "access_token": "<google id token>" }
    Verifies the token, gets-or-creates the user, returns our own JWT pair —
    mirrors the shape of the username/password login response.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = GoogleExchangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            payload = services.verify_google_token(serializer.validated_data["access_token"])
        except services.InvalidGoogleToken:
            return Response({"detail": "Invalid Google token."}, status=status.HTTP_401_UNAUTHORIZED)

        user, _created = services.get_or_create_user_from_google(payload)
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            }
        )