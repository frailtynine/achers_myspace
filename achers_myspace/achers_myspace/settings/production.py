from .base import *

# Add PostgreSQL support for production
INSTALLED_APPS = INSTALLED_APPS + ["django.contrib.postgres"]

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/6.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# In production, Django will store uploaded files in a persistent volume at /app/media
MEDIA_ROOT = "/app/media"

try:
    from .local import *
except ImportError:
    pass
