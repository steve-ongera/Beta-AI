# ============================================================================
# App:  config (project-level, not one of the 4 local apps)
# File: urls.py  (root URLConf)
# Role: Each domain (auth, chat, media, modules) is namespaced so future
#       modules register the same way the mentalhealth module does.
# ============================================================================

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # --- users app: auth (username/password + Google OAuth) ---------------
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/auth/", include("users.urls")),  # custom endpoints (google exchange, /me)

    # --- chat app: module registry + cross-module history -----------------
    path("api/modules/", include("chat.urls")),

    # --- media_ai app: image upload + image generation ---------------------
    path("api/media/", include("media_ai.urls")),

    # --- mentalhealth app: first pluggable AI app module -------------------
    path("api/modules/mental-health/", include("mentalhealth.urls")),

    # Future modules register the same way, e.g.:
    # path("api/modules/nutrition/", include("nutrition.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)