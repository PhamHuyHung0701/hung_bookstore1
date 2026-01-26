"""
Django settings for API Gateway
Runs on PORT 8000 - Main Web Interface
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'api-gateway-secret-key-12345'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'gateway',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

# Shared database for all 3 projects (Monolithic, cleanArchitecture, Microservices)
SHARED_DB_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / 'shared_db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': SHARED_DB_PATH,
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Service Configuration
SERVICE_NAME = 'api-gateway'
SERVICE_PORT = 8000

# Microservices URLs
CUSTOMER_SERVICE_URL = 'http://localhost:8001'
BOOK_SERVICE_URL = 'http://localhost:8002'
CART_SERVICE_URL = 'http://localhost:8003'
