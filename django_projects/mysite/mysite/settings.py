"""
Configuración de Django para el proyecto 'mysite'.

Generado por 'django-admin startproject' con Django 4.0.7.
Para más información, consulta:
- General: https://docs.djangoproject.com/en/4.0/topics/settings/
- Lista de configuraciones: https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
import logging
logging.basicConfig(level=logging.DEBUG)
# Directorio base del proyecto (mysite/)
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
# Nombre de la aplicación
APP_NAME = 'Carlos Saenz'

# Clave secreta (¡cámbiala en producción!)
SECRET_KEY = 'django-insecure-z9lrp*)$e7hyx-v&48uu%@1&ab8%2vq3ohoptt!a6@6=)uj(5*'

# Modo debug (desactiva en producción)
DEBUG = True

# Hosts permitidos (ajústalos en producción)
ALLOWED_HOSTS = ['*']

# Aplicaciones instaladas
INSTALLED_APPS = [
    # Apps de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Extensiones de terceros
    'django_extensions',
    'crispy_forms',
    'rest_framework',
    'social_django',
    'taggit',
    'bootstrap3',

    # Apps personalizadas
    'polls.apps.PollsConfig',
    'home.apps.HomeConfig',
    'hello.apps.HelloConfig',
    'autos.apps.AutosConfig',
    'authz.apps.AuthzConfig',
    'cats.apps.CatsConfig',
    'api_xm',
]

# Configuración de Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs raíz
ROOT_URLCONF = 'mysite.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'mysite', 'templates')],  # Directorio global para base.html
        'APP_DIRS': True,  # Busca en <app>/templates/ (ej. api_xm/templates/)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.settings',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

# Aplicación WSGI
WSGI_APPLICATION = 'mysite.wsgi.application'

# Base de datos (SQLite para desarrollo)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

# Configuración adicional para desarrollo
if DEBUG:
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"Templates DIRS: {os.path.join(BASE_DIR)}")#, 'mysite', 'templates'
    print(f"STATICFILES_DIRS: {STATICFILES_DIRS}")
# Configuración de REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# Autenticación social (GitHub)
try:
    from . import github_settings
    SOCIAL_AUTH_GITHUB_KEY = github_settings.SOCIAL_AUTH_GITHUB_KEY
    SOCIAL_AUTH_GITHUB_SECRET = github_settings.SOCIAL_AUTH_GITHUB_SECRET
except ImportError:
    print("Configura 'github_settings.py' para habilitar login social con GitHub")

# Backends de autenticación
AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Redirecciones de login/logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Tipo de campo automático por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración adicional para desarrollo
if DEBUG:
    # Imprimir rutas para depuración
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"Templates DIRS: {os.path.join(BASE_DIR, 'mysite', 'templates')}")