import os
import sys
import environ
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

ENV = environ.Env(DEBUG=(bool, False))

ENV_FILE = Path(os.path.join(BASE_DIR, ".env"))
if ENV_FILE.exists():
    environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

DEBUG = ENV.bool("DEBUG", False)
SECRET_KEY = ENV.str("SECRET_KEY")
ALLOWED_HOSTS = ENV.list("ALLOWED_HOSTS", default=[])

CORE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


EXTERNAL_APPS = [
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "corsheaders",
]

PROJECT_APPS = ["apps.users", "apps.tracking"]

INSTALLED_APPS = CORE_APPS + EXTERNAL_APPS + PROJECT_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "asystem.wsgi.application"

CSRF_COOKIE_HTTPONLY = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": ENV.str("DB_NAME"),
        "USER": ENV.str("DB_USER"),
        "PASSWORD": ENV.str("DB_PASSWORD"),
        "HOST": ENV.str("DB_HOST"),
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "users.User"

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Almaty"

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.domain\.com$",
]
CSRF_TRUSTED_ORIGINS = ["*"]
CORS_ALLOWED_ORIGINS = ["*"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

FRONTEND_URL = ENV.str("FRONTEND_URL")
DEFAULT_FROM_EMAIL = ENV.str("DEFAULT_FROM_EMAIL", default="")

EMAIL_CONFIG = ENV.email_url("EMAIL_URL", default="")
vars().update(EMAIL_CONFIG)
DEFAULT_FROM_EMAIL = ENV.str("DEFAULT_FROM_EMAIL", default="")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}


SMS_PROVIDER_URL = ENV.str("SMS_PROVIDER_URL")
SMS_PROVIDER_USERNAME = ENV.str("SMS_PROVIDER_USERNAME")
SMS_PROVIDER_PASSWORD = ENV.str("SMS_PROVIDER_PASSWORD")
SMS_CODE_TTL = ENV.float("SMS_CODE_TTL")
