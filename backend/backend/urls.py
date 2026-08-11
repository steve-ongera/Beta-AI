"""
Main URL configuration. Each domain (auth, chat, media, modules) is namespaced
so future modules register the same way the mental_health module does.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth: username/password + Google OAuth (dj-rest-auth + allauth)
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/auth/", include("users.urls")),  # custom endpoints (google exchange, refresh helpers)

    # Core platform
    path("api/chat/", include("chat.urls")),
    path("api/media/", include("media_ai.urls")),

    # Pluggable AI app modules — each module owns its own urls.py
    path("api/modules/mental-health/", include("modules.mental_health.urls")),

    # Future modules register here, e.g.:
    # path("api/modules/nutrition/", include("modules.nutrition.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)