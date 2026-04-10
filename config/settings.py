import logging
import os
from pathlib import Path

from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=False)
logger.info("DEBUG: " + str(DEBUG))

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
logger.info("ALLOWED_HOSTS: " + str(ALLOWED_HOSTS))

# APPLICATION SECURITY
SECURE_HSTS_SECONDS = 3600  # 1 hour
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", cast=bool, default=False)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", cast=bool, default=True)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", cast=bool, default=True)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS", cast=lambda v: [s.strip() for s in v.split(",")], default=[]
)

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# THIRD_PARTY_APPS = [

# ]

# Custom apps
# CUSTOM_APPS = [
#     # Add your custom apps here
# ]

INSTALLED_APPS = DJANGO_APPS  # + THIRD_PARTY_APPS + CUSTOM_APPS


# AUTHENTICATION_BACKENDS  = [
#     'axes.backends.AxesStandaloneBackend',
#     'django.contrib.auth.backends.ModelBackend',
#     'guardian.backends.ObjectPermissionBackend',
# ]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {}
USE_SQLITE = config("USE_SQLITE", cast=bool, default=True)
USE_MYSQL = config("USE_MYSQL",  cast=bool, default=False)
USE_POSTGRES = config("USE_POSTGRES",  cast=bool, default=False)

if USE_SQLITE:
    logger.info(f"USE_SQLITE: {USE_SQLITE}")
    DATABASES.update(
        {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }
    )
elif USE_MYSQL:
    logger.info(f"USE_MYSQL: {USE_MYSQL}")
    DATABASES.update(
        {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": config("MYSQL_NAME"),
                "USER": config("MYSQL_USERNAME"),
                "HOST": config("MYSQL_HOST"),
                "PORT": config("MYSQL_PORT"),
                "PASSWORD": config("MYSQL_PASSWORD"),
            }
        }
    )
elif USE_POSTGRES:
    logger.info(f"USE_POSTGRES: {USE_POSTGRES}")
    DATABASES.update(
        {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": config("POSTGRES_NAME"),
                "USER": config("POSTGRES_USERNAME"),
                "HOST": config("POSTGRES_HOST"),
                "PORT": config("POSTGRES_PORT"),
                "PASSWORD": config("POSTGRES_PASSWORD"),
            }
        }
    )
else:
    logger.error("No Database configured")


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = config("STATIC_ROOT", default=os.path.join(BASE_DIR, "static"))

MEDIA_URL = "/media/"
MEDIA_ROOT = config("MEDIA_ROOT", default=os.path.join(BASE_DIR, "media"))

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {"format": "{levelname} {message}", "style": "{"},
    },
    "handlers": {
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "simple"},
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {"handlers": ["console", "file"], "level": "INFO", "propagate": True},
        # customize logs for apps
        "*": {"handlers": ["console", "file"], "level": "INFO", "propagrate": True},
    },
}
