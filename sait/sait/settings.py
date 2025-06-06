# settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------------------------------
# НЕОБХОДИМО ДЛЯ ЛОКАЛЬНОЙ РАЗРАБОТКИ:
DEBUG = True

# При DEBUG=False сюда нужно добавить уже реальные хосты, например:
# DEBUG = False
# ALLOWED_HOSTS = ["yourdomain.com", "www.yourdomain.com"]
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    # если вы планируете запускать через ngrok, нужно указать и ngrok-домен:
    # "xxxxxxxx.ngrok-free.app",
]

# --------------------------------------------------------------------------------------------------
# Секретный ключ. В продакшне лучше читать из переменных окружения, но для локального запуска можно оставить «по умолчанию».
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "локальный_фолбек_для_разработки")
# --------------------------------------------------------------------------------------------------

INSTALLED_APPS = [
    "main",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sait.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Если у вас есть общая папка верхнего уровня «templates», раскомментируйте и добавьте:
        # "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "sait.wsgi.application"

# Если нигде не меняли, оставляем sqlite3
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------ СТАТИКА ------------------

STATIC_URL = "/static/"

# Убедитесь, что у вас реально существует папка <BASE_DIR>/static,
# внутри которой лежат ваши CSS/JS/изображения:
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# и все файлы скопируются в STATIC_ROOT:
STATIC_ROOT = BASE_DIR / "staticfiles"

# ------------------ МЕДИА ------------------

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
