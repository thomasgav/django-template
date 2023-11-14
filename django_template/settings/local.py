from .base import * #noqa
from .base import env

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="TsxTLO1lIi7ofpucSucZLOUQWx-QBDUlkSzBzXKjxi3EKoM3xsQ"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]
