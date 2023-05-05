from . base import *

ALLOWED_HOSTS = [
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEBUG=True

STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []