import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-key-for-development-only")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "www.uzmovi.asia", "uzmovi.asia", "localhost"]

# Application definition
INSTALLED_APPS = [
    # 'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
     'django.contrib.sitemaps',
    # Third-party apps
    "crispy_forms",
    "crispy_bootstrap5",
    "mptt",
    "taggit",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_cleanup.apps.CleanupConfig",
    # Local apps
    "movies.apps.MoviesConfig",
    "users.apps.UsersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = "Uzmovi.urls"

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
                "movies.context_processors.categories",
            ],
            "libraries": {
                "custom_tags": "movies.templatetags.custom_tags",
            },
        },
    },
]

WSGI_APPLICATION = "Uzmovi.wsgi.application"

# Database
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "uzmovi_db",
        "USER": "uzmovi",
        "PASSWORD": "Uzmovi2025",
        "HOST": "localhost",
        "PORT": "",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
LANGUAGE_CODE = "uz"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication settings
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
LOGIN_URL = "account_login"

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email settings (for development)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # Or your email provider's SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv(
    "EMAIL_HOST_USER", "buyupuz@gmail.com"
)  # Set this in your environment variables
EMAIL_HOST_PASSWORD = os.getenv(
    "EMAIL_HOST_PASSWORD", "fxjudtbynsascgra"
)  # Set this in your environment variables
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "buyupuz@gmail.com")

# Django AllAuth settings
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_PASSWORD_MIN_LENGTH = 8
# Remove complexity requirements
ACCOUNT_PASSWORD_COMPLEXITY_VALIDATION = None
# Add this to your settings.py to make username not unique
AUTH_USER_MODEL = "auth.User"
