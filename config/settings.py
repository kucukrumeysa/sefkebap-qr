from pathlib import Path
from decouple import config
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-sef-kebab-secret-key-change-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='sefkebap-qr.vercel.app,localhost,127.0.0.1').split(',')

# Production Security Settings
if not DEBUG:
    # Ensure a proper secret key is set in production
    if SECRET_KEY == 'django-insecure-sef-kebab-secret-key-change-in-production':
        raise ValueError("SECRET_KEY must be changed in production!")
        
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'same-origin'
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS Settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    # Local Development Security Settings
    X_FRAME_OPTIONS = 'SAMEORIGIN'


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'apps.menu',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.menu.context_processors.restaurant_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASE_URL = os.environ.get('DATABASE_URL') or config('DATABASE_URL', default=None)

if DATABASE_URL and (DATABASE_URL.startswith('postgres://') or DATABASE_URL.startswith('postgresql://')):
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'tr-tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Restaurant settings
RESTAURANT_NAME = config('RESTAURANT_NAME', default='Şef Kebap')
RESTAURANT_PHONE = config('RESTAURANT_PHONE', default='(0322) 226 00 11')
RESTAURANT_ADDRESS = config('RESTAURANT_ADDRESS', default='Yenibaraj, Seyhan / Adana')
RESTAURANT_WHATSAPP = config('RESTAURANT_WHATSAPP', default='903222260011')
RESTAURANT_MAPS_URL = config('RESTAURANT_MAPS_URL', default='https://maps.app.goo.gl/ZszCdqTErwmiDmbD8')
RESTAURANT_OPEN_TIME = config('RESTAURANT_OPEN_TIME', default='09:00')
RESTAURANT_CLOSE_TIME = config('RESTAURANT_CLOSE_TIME', default='00:00')
MENU_URL = config('MENU_URL', default='http://localhost:8000/menu/')

# Jazzmin Admin Panel Customization (Bright/Light Theme)
JAZZMIN_SETTINGS = {
    "site_title": "Şef Kebap Yönetim Paneli",
    "site_header": "Şef Kebap",
    "site_brand": "Şef Kebap",
    "welcome_sign": "Şef Kebap Menü Yönetimine Hoş Geldiniz",
    "copyright": "Şef Kebap",
    "search_model": "menu.Product",
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "menu.category": "fas fa-list",
        "menu.subcategory": "fas fa-indent",
        "menu.product": "fas fa-utensils",
    },
    "order_with_respect_to": ["menu", "menu.category", "menu.subcategory", "menu.product", "auth"],
    "topmenu_links": [
        {"name": "Yönetim Paneli", "url": "admin:index"},
        {"name": "Canlı Menüyü Gör", "url": "/menu/", "new_window": True},
    ],
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_color": "navbar-light",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",  # A clean, cheerful, bright light-mode bootstrap theme
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

