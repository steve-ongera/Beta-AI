# ============================================================================
# App:  config (project-level, not one of the 4 local apps)
# File: settings.py
# Role: Django settings for MindBridge AI platform. Split-ready: everything
#       env-driven so this can later become base/dev/prod settings.
# ============================================================================

import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Third-party
    "rest_framework",
    "rest_framework.authtoken",  # required by dj-rest-auth even when using JWT (see REST_AUTH below)
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",  # needed for SIMPLE_JWT's BLACKLIST_AFTER_ROTATION below
    "corsheaders",
    "django_filters",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "dj_rest_auth",
    "dj_rest_auth.registration",

    # Local apps (4)
    "users",         # auth: username/password + Google OAuth, user profile
    "chat",          # module registry + cross-module chat history aggregation
    "media_ai",      # image upload analysis + image generation
    "mentalhealth",  # first AI app module: mental health chat
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"
ASGI_APPLICATION = "backend.asgi.application"

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    # {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# REST Framework / JWT
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",  # per-view overrides for guest access
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "guest-chat": "20/hour",
        "auth-chat": "200/hour",
        "image-gen": "30/hour",
        # dj-rest-auth's own views (login, registration, password reset,
        # ...) declare their own throttle_scope. DRF requires a rate for
        # EVERY scope any view uses — including ones from third-party
        # packages we didn't define ourselves — or it raises
        # ImproperlyConfigured the first time that view is hit. These two
        # entries are what fixes that error.
        "dj_rest_auth": "20/minute",
        "dj_rest_auth_registration": "10/minute",
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# dj-rest-auth's get_token_model() runs at import time and requires
# rest_framework.authtoken in INSTALLED_APPS (added above) regardless of
# REST_USE_JWT in this version — that app is what actually fixes the
# ImproperlyConfigured crash. USE_JWT below just makes dj-rest-auth's
# login/logout views return JWTs instead of a legacy auth token.
REST_USE_JWT = True
JWT_AUTH_HTTPONLY = False  # frontend/src/services/api.js reads the JSON body, not a cookie
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
}

# ---------------------------------------------------------------------------
# CORS (React dev server)
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS", "http://localhost:5173"
).split(",")
CORS_ALLOW_CREDENTIALS = True

# ---------------------------------------------------------------------------
# Google OAuth (django-allauth)
# ---------------------------------------------------------------------------
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.environ.get("GOOGLE_OAUTH_CLIENT_ID", ""),
            "secret": os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", ""),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
    }
}
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_LOGIN_METHODS = {"email", "username"}

# ---------------------------------------------------------------------------
# Email
# Registration/password-reset flows send email even when verification is
# "optional". Without an EMAIL_BACKEND, Django defaults to SMTP on
# localhost:25, which nothing is listening on in dev — that's what caused
# ConnectionRefusedError. Console backend just prints the email to your
# runserver terminal instead of actually sending it. Swap to SMTP in
# production by setting EMAIL_HOST etc. via env vars.
# ---------------------------------------------------------------------------
if DEBUG and not os.environ.get("EMAIL_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@mindbridge.local")

# ---------------------------------------------------------------------------
# AI Engine / external services (decoupled inference service)
# ---------------------------------------------------------------------------
AI_ENGINE_URL = os.environ.get("AI_ENGINE_URL", "http://localhost:9000")
AI_ENGINE_TIMEOUT_SECONDS = int(os.environ.get("AI_ENGINE_TIMEOUT_SECONDS", "30"))
IMAGE_GEN_SERVICE_URL = os.environ.get("IMAGE_GEN_SERVICE_URL", "http://localhost:9100")

# Crisis-safety: keywords/resources used by mentalhealth.services
CRISIS_ESCALATION_WEBHOOK = os.environ.get("CRISIS_ESCALATION_WEBHOOK", "")

# ---------------------------------------------------------------------------
# Celery / Redis
# ---------------------------------------------------------------------------
CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "redis://localhost:6379/0")