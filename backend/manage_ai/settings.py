from datetime import timedelta
from pathlib import Path
import os

import dj_database_url
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env only for local development.
if (BASE_DIR / ".env").exists():
    load_dotenv(BASE_DIR / ".env")


def env(name: str, default: object = None) -> str | None:
    value = os.getenv(name)
    if value is not None:
        return value
    if default is None:
        return None
    return str(default)


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def env_int(name: str, default: int) -> int:
    value = env(name)
    if value is None:
        return default
    return int(value)


def csv_env(name: str, default: str = "") -> list[str]:
    raw_value = env(name, default) or default
    return [item.strip() for item in raw_value.split(",") if item.strip()]


SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-only-change-me") or "dev-only-change-me"
DEBUG = env_bool("DJANGO_DEBUG", False)

_railway_domain = env("RAILWAY_PUBLIC_DOMAIN", "") or ""
_railway_static_url = env("RAILWAY_STATIC_URL", "") or ""
_extra_hosts = env("DJANGO_ALLOWED_HOSTS", "") or ""

_base_hosts = ["localhost", "127.0.0.1", "0.0.0.0", "[::1]"]
if _railway_domain:
    _base_hosts.append(_railway_domain)
if _railway_static_url:
    _base_hosts.append(_railway_static_url)
_base_hosts.append(".railway.app")
_base_hosts.append(".up.railway.app")
if _extra_hosts:
    for host in _extra_hosts.split(","):
        host = host.strip()
        if host:
            _base_hosts.append(host)

ALLOWED_HOSTS = list(dict.fromkeys(_base_hosts))

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "django_filters",
    "corsheaders",
    "channels",
    "apps.accounts",
    "apps.projects",
    "apps.tasks",
    "apps.tickets",
    "apps.deployments",
    "apps.documents",
    "apps.notifications",
    "apps.audit",
    "apps.analytics",
    "apps.ai",
    "apps.enterprise",
    "apps.realtime",
    "apps.core",
    "apps.users",
    "apps.modules",
    "apps.crm",
    "apps.erp",
    "apps.hr",
    "apps.inventory",
    "apps.file_tracking",
    "apps.webhooks",
    "apps.ai_layer",
    "apps.server_monitor",
    "apps.api_keys",
    "apps.hosting",
    "apps.api_monitor",
    "apps.remote_access",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.api_keys.middleware.ApiKeyMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.audit.middleware.APIRequestLoggingMiddleware",
]

ROOT_URLCONF = "manage_ai.urls"

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

WSGI_APPLICATION = "manage_ai.wsgi.application"
ASGI_APPLICATION = "manage_ai.asgi.application"

DATABASE_URL = env("DATABASE_URL")
if DATABASE_URL:
    database_config = dj_database_url.parse(DATABASE_URL, conn_max_age=env_int("DB_CONN_MAX_AGE", 60))
    database_options = dict(database_config.get("OPTIONS") or {})
    host = str(database_config.get("HOST", ""))
    if host not in {"localhost", "127.0.0.1", "::1", ""}:
        database_options["sslmode"] = "require"
    database_config["OPTIONS"] = database_options
    DATABASES = {
        "default": database_config,
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / (env("DB_NAME", "manageai.sqlite3") or "manageai.sqlite3"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DATA_UPLOAD_MAX_MEMORY_SIZE = env_int("DATA_UPLOAD_MAX_MEMORY_SIZE", 5 * 1024 * 1024 * 1024)
FILE_UPLOAD_MAX_MEMORY_SIZE = env_int("FILE_UPLOAD_MAX_MEMORY_SIZE", 10 * 1024 * 1024)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "URL_FORMAT_OVERRIDE": None,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env_int("ACCESS_TOKEN_MINUTES", 30)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env_int("REFRESH_TOKEN_DAYS", 7)),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

CORS_ALLOWED_ORIGINS = [o.strip() for o in (env("CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174,http://localhost:5175,http://127.0.0.1:5175") or "").split(",") if o.strip()]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [o.strip() for o in (env("CSRF_TRUSTED_ORIGINS", "") or "").split(",") if o.strip()]
if _railway_domain:
    railway_https = f"https://{_railway_domain}"
    if railway_https not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(railway_https)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

if not DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

_redis_url = env("REDIS_URL", "") or ""
_use_inmemory = env_bool("USE_INMEMORY_CHANNELS", not bool(_redis_url))
_channel_layers = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}} if _use_inmemory else {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [_redis_url]},
    }
}

CHANNEL_LAYERS = _channel_layers

_redis_cache_url = env("REDIS_CACHE_URL", env("REDIS_URL", "")) or ""
_caches = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": _redis_cache_url,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
} if _redis_cache_url else {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

CACHES = _caches

AI_PROVIDER = env("AI_PROVIDER", "local")
AI_ENABLED = env_bool("AI_ENABLED", False)
ANTHROPIC_API_KEY = env("ANTHROPIC_API_KEY", "")
FIELD_ENCRYPTION_KEY = env("FIELD_ENCRYPTION_KEY", "")
GITHUB_TOKEN = env("GITHUB_TOKEN", "")
VERCEL_API_TOKEN = env("VERCEL_API_TOKEN", env("VERCEL_TOKEN", ""))
VERCEL_TEAM_ID = env("VERCEL_TEAM_ID", "")
VERCEL_CACHE_SECONDS = env_int("VERCEL_CACHE_SECONDS", 45)
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", env("AWS_ACCESS_KEY", ""))
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", env("AWS_SECRET_KEY", ""))
AWS_REGION = env("AWS_REGION", "us-east-1")
NETLIFY_API_TOKEN = env("NETLIFY_API_TOKEN", env("NETLIFY_TOKEN", ""))
CLOUDFLARE_API_TOKEN = env("CLOUDFLARE_API_TOKEN", "")
DIGITALOCEAN_API_TOKEN = env("DIGITALOCEAN_API_TOKEN", "")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "ManageAI <noreply@manageai.local>")
EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")

SPECTACULAR_SETTINGS = {
    "TITLE": "Universal Connection Engine API",
    "DESCRIPTION": "Unified CRM, ERP, HR, Inventory, Project Management, event, and optional AI APIs.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

CELERY_BROKER_URL = env("CELERY_BROKER_URL", env("REDIS_URL", "redis://127.0.0.1:6379/0"))
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", CELERY_BROKER_URL)
CELERY_TASK_ALWAYS_EAGER = env_bool("CELERY_TASK_ALWAYS_EAGER", DEBUG)
API_KEY_FERNET_KEY = env("API_KEY_FERNET_KEY", FIELD_ENCRYPTION_KEY)

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "check-expiry-daily": {"task": "apps.notifications.tasks.check_hosting_expiry", "schedule": crontab(hour=9, minute=0)},
    "hosting-health-checks": {"task": "hosting.tasks.check_all_hosted_project_health", "schedule": 60.0},
    "hosting-vercel-sync": {"task": "hosting.tasks.sync_vercel_projects", "schedule": 60.0},
    "hosting-provider-sync": {"task": "hosting.tasks.sync_all_hosting_providers", "schedule": 120.0},
    "hosting-provider-failover": {"task": "hosting.tasks.evaluate_hosting_failover", "schedule": 60.0},
    "hosting-vercel-link-checks": {"task": "hosting.tasks.check_vercel_links", "schedule": 60.0},
    "hosting-vercel-deployment-alerts": {"task": "hosting.tasks.notify_failed_vercel_deployments", "schedule": 300.0},
    "hosting-lifecycle-statuses": {"task": "hosting.tasks.update_hosting_lifecycle_statuses", "schedule": crontab(hour=9, minute=10)},
    "collect-metrics": {"task": "apps.server_monitor.tasks.collect_server_metrics", "schedule": 60.0},
    "check-disk-alerts": {"task": "apps.server_monitor.tasks.check_disk_alerts", "schedule": 300.0},
    "broadcast-api-stats": {"task": "apps.api_monitor.tasks.broadcast_api_stats", "schedule": 10.0},
}
