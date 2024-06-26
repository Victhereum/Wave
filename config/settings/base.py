"""
Base settings to build other settings files upon.
"""
from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# wave/
APPS_DIR = BASE_DIR / "wave"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
TESTING = env.bool("TESTING", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#languages
# from django.utils.translation import gettext_lazy as _
# LANGUAGES = [
#     ('en', _('English')),
#     ('pt-br', _('Português')),
# ]
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}

DATABASES["default"]["ATOMIC_REQUESTS"] = True
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    "django_celery_beat",
    "rest_framework",
    "djoser",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
]

LOCAL_APPS = [
    "wave.apps.users.apps.UsersConfig",
    "wave.apps.payments.apps.SubscriptionsConfig",
    "wave.apps.video.apps.CaptionConfig",
    # Your stuff: custom apps go here
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "wave.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"
# DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400
# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # "wave.users.context_processors.allauth_settings",
            ],
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Victor Isaac""", "victor-isaac@wavesa.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# https://cookiecutter-django.readthedocs.io/en/latest/settings.html#other-environment-settings
# Force the `admin` sign in process to go through the `django-allauth` workflow
# DJANGO_ADMIN_FORCE_ALLAUTH = env.bool("DJANGO_ADMIN_FORCE_ALLAUTH", default=False)

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Celery
# ------------------------------------------------------------------------------
# if USE_TZ:
#     # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
#     CELERY_TIMEZONE = TIME_ZONE
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
# CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6377") or env("REDIS_URL")
# REDIS_CA_CERT_FILE_PATH: str = env("REDIS_CA_CERT_FILE_PATH", default=None)
# REDIS_CA_CERT_FILE_EXISTS = REDIS_CA_CERT_FILE_PATH and os.path.exists(REDIS_CA_CERT_FILE_PATH)
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
# CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# REDIS_IS_USING_SSL = CELERY_RESULT_BACKEND.startswith("rediss")
# if REDIS_IS_USING_SSL:
#     SSL_KWARGS = dict(ssl_cert_reqs=ssl.CERT_NONE)

#     if REDIS_CA_CERT_FILE_EXISTS:
#         SSL_KWARGS["ssl_cert_reqs"] = ssl.CERT_REQUIRED
#         SSL_KWARGS["ssl_ca_certs"] = REDIS_CA_CERT_FILE_PATH

#     # CELERY_BROKER_USE_SSL = CELERY_REDIS_BACKEND_USE_SSL = SSL_KWARGS
#     CELERY_REDIS_BACKEND_USE_SSL = SSL_KWARGS
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
# CELERY_RESULT_EXTENDED = True
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
# # https://github.com/celery/celery/pull/6122
# CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
# CELERY_RESULT_BACKEND_MAX_RETRIES = 10
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
# CELERY_ACCEPT_CONTENT = ["json"]
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
# CELERY_TASK_SERIALIZER = "json"
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
# CELERY_RESULT_SERIALIZER = "json"
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# # TODO: set to whatever value is adequate in your circumstances
# CELERY_TASK_TIME_LIMIT = 5 * 60
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# # TODO: set to whatever value is adequate in your circumstances
# CELERY_TASK_SOFT_TIME_LIMIT = 60
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
# CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
# CELERY_WORKER_SEND_TASK_EVENTS = True
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
# CELERY_TASK_SEND_SENT_EVENT = True

# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]
# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {"AUTH_HEADER_TYPES": ("Bearer",), "ACCESS_TOKEN_LIFETIME": timedelta(days=30)}
# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"

# By Default swagger ui is available only to admin user(s). You can change permission classes to change that
# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Wave API",
    "DESCRIPTION": "Documentation of API endpoints of Wave",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
}
# Your stuff...
# ------------------------------------------------------------------------------
API_VERSION = env("API_VERSION", default="v1")
TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID", default="xxx")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN", default="xxx")
TWILIO_PHONE = env("TWILIO_PHONE", default="xxx")
MOYASAR_API_KEY = env("MOYASAR_API_KEY", default="xxx")
MAX_VIDEO_SIZE = 25_000_000
OPEN_AI_KEY = env("OPEN_AI_KEY", default="xxx")
AZURE_SERVICE_KEY = env("AZURE_SERVICE_KEY", default="xxx")
AZURE_TEXT_SERVICE_KEY = env("AZURE_TEXT_SERVICE_KEY", default="xxx")
AZURE_SERVICE_REGION = env("AZURE_SERVICE_REGION", default="xxx")
AZURE_SERVICE_ENDPOINT = env("AZURE_SERVICE_ENDPOINT", default="xxx")
AZURE_TEXT_SERVICE_ENDPOINT = env("AZURE_TEXT_SERVICE_ENDPOINT", default="xxx")
USE_TWILIO = env("USE_TWILIO", default=True)
BASIC_PLAN_PRICE = env.float("BASIC_PLAN_PRICE", default=1.00)
PRO_PLAN_PRICE = env.float("PRO_PLAN_PRICE", default=1.00)
PREMIUM_PLAN_PRICE = env.float("PREMIUM_PLAN_PRICE", default=1.00)

ACCESS_STRUCTURE = {
    "TRIAL": {
        "COUNT": env.int("TRIAL_COUNT", default=2),
        "LENGTH": timedelta(minutes=env.int("TRIAL_LENGTH", default=1)).total_seconds(),
    },
    "BASIC": {
        "COUNT": env.int("BASIC_COUNT", default=10),
        "LENGTH": timedelta(minutes=env.int("BASIC_LENGTH", default=5)).total_seconds(),
    },
    "PRO": {
        "COUNT": env.int("PRO_COUNT", default=30),
        "LENGTH": timedelta(minutes=env.int("PRO_LENGTH", default=5)).total_seconds(),
    },
    "PREMIUM": {
        "COUNT": env.int("PREMIUM_COUNT", default=50),
        "LENGTH": timedelta(minutes=env.int("PREMIUM_LENGTH", default=5)).total_seconds(),
    },
}
DATA_UPLOAD_MAX_MEMORY_SIZE = 300_097_152
FILE_UPLOAD_MAX_MEMORY_SIZE = DATA_UPLOAD_MAX_MEMORY_SIZE
BUNNY_ACCESS_KEY = env("BUNNY_ACCESS_KEY")
STORAGE_ZONE_NAME = env("STORAGE_ZONE_NAME")
