"""
Django settings for Cart Service
Runs on PORT 8003
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'cart-service-secret-key-12345'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'rest_framework',
    'corsheaders',
    'carts',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'config.urls'

# Shared database for all 3 projects (Monolithic, cleanArchitecture, Microservices)
SHARED_DB_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / 'shared_db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': SHARED_DB_PATH,
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

# Service Configuration
SERVICE_NAME = 'cart-service'
SERVICE_PORT = 8003

# Other Services URLs
CUSTOMER_SERVICE_URL = 'http://localhost:8001'
BOOK_SERVICE_URL = 'http://localhost:8002'
