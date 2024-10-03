"""
Django settings for insuradmin_backend project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)

# Change for Build ofc
# ALLOWED_HOSTS = [".herokuapp.com", "localhost", "127.0.0.1"]
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles", 
    "django.contrib.sites",
    # External
    "axes",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "corsheaders",
    "crispy_forms",
    "crispy_bootstrap5",
    "debug_toolbar",
    "django_recaptcha",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "django_twilio",
    # "django_otp",
    # "django_otp.plugins.otp_static",
    # "django_otp.plugins.otp_totp",
    # "django_otp.plugins.otp_email",
    "drf_spectacular",
    # "two_factor",
    # "two_factor.plugins.phonenumber",
    # "two_factor.plugins.email",
    "rest_framework",
    "rest_framework.authtoken",
    # Local
    "accounts.apps.AccountsConfig",
    "insurances.apps.InsurancesConfig",
    "pages.apps.PagesConfig",
    "processes.apps.ProcessesConfig",
    "assistant.apps.AssistantConfig",
]

MIDDLEWARE = [
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # place corsheaders before any middleware that can generate responses
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django_otp.middleware.OTPMiddleware", # 2FA
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_auto_logout.middleware.auto_logout", # Auto logout
    "axes.middleware.AxesMiddleware", # Brute Force
    # "two_factor.middleware.threadlocals.ThreadLocals", # Twilio Gateway
]

ROOT_URLCONF = "insuradmin_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                # Auto logout
                "django_auto_logout.context_processors.auto_logout_client",
            ],
        },
    },
]

WSGI_APPLICATION = "insuradmin_backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": env.dj_db_url("DATABASE_URL",
    default="postgres://postgres@db/postgres")
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

## Time Zone List: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
# DE is "Europe/Berlin"
# Default: TIME_ZONE = "UTC"
TIME_ZONE = "Europe/Berlin"
## Set True to use UTC on data / False for local time
USE_TZ = True

## Django Translations
USE_I18N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    ]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.CustomUser"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# # # LEGACY CODE REST_FRAMEWORK --- "mvp0001" --- :
# # Pagination allows you to control how many objects per page are returned
# REST_FRAMEWORK = {
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": 10,
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
#     "EXCEPTION_HANDLER": "account.exceptionhandler.status_code_handler",
# }

# Cross-origin resource sharing (CORS)
CORS_ORIGIN_WHITELIST = (
    # React regular
    "http://localhost:3000",
    # Backend regular
    "http://localhost:8000",
)

# Cross-Site Request Forgery (CSRF)
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]
# # LEGACY CODE "mvp0001":
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = True

# django-crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# # 2FA
# LOGIN_URL = "two_factor:login"
# # # this one is optional
# # LOGIN_REDIRECT_URL = 'two_factor:profile'

LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'account_data_list'
LOGOUT_REDIRECT_URL = 'account_login'
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "axes.backends.AxesStandaloneBackend",
)

ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

# Email Settings
EMAIL_BACKEND = env("EMAIL_BACKEND")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

# drf-spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "Insurance API Project",
    "DESCRIPTION": "A sample blog to learn about Insurances",
    "VERSION": "1.0.0",
    # OTHER SETTINGS
}

# OpenAI Integration API
OPENAI_API_KEY = env("OPENAI_API_KEY")

# Info Toast Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Recaptcha Keys
# Recaptcha
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")
NOCAPTCHA = True


### Handle the Redirect correct for logout
# Auto logout
# from datetime import timedelta

# AUTO_LOGOUT = {
#     'IDLE_TIME': timedelta(minutes=10),
#     'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
# }

AUTO_LOGOUT = {
    'SESSION_TIME': 3600,
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
    'MESSAGE': 'The session has expired. Please login again to continue.',
}  # logout after 15 seconds


# Axes configuration
AXES_FAILURE_LIMIT: 3 # How many times a user can fail login
AXES_COOLOFF_TIME: 1 # Wait 1 hour before attempting to login again
# python manage.py axes_reset for manually reset
# Reset on success to set back the attempts to 0
AXES_RESET_ON_SUCCESS = True # Reset failed login attempts
AXES_LOCKOUT_TEMPLATE = 'accounts/account_locked.html' # Add a custom template

# # Other AXES Configurations - Blocking User instead of IP-Adress
# AXES_FAILURE_LIMIT = 5  # Anzahl der erlaubten fehlgeschlagenen Versuche
# AXES_COOLOFF_TIME = 1  # Abkühlzeit in Stunden
# AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True  # Sperre pro Kombination aus Benutzername und IP
# AXES_RESET_ON_SUCCESS = True  # Rücksetzen der fehlgeschlagenen Versuche bei erfolgreicher Anmeldung
# AXES_LOCKOUT_TEMPLATE = 'accounts/account_locked.html'  # Sperrvorlage
# AXES_LOGGER = 'axes.watch_login'  # Protokollierung
# AXES_VERBOSE = True  # Ausführliche Protokollierung


# Twilio 2FA
# TWO_FACTOR_SMS_GATEWAY = 'two_factor.gateways.twilio.gateway.Twilio'
TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_VERIFICATION_SERVICE_SID = env("TWILIO_VERIFICATION_SERVICE_SID")
TWILIO_CALLER_ID = env("TWILIO_CALLER_ID")


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# SendGrid
SENDGRID_API_KEY = env("SENDGRID_API_KEY")