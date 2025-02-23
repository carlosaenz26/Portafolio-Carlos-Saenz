"""
Configuración de URLs para el proyecto mysite.

Este archivo define las rutas URL del proyecto, mapeando URLs a vistas o incluyendo URLconfs de otras aplicaciones.
Para más detalles, consulta: https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings
from django.contrib.auth import views as auth_views
from home.views import HomeView
import os

# Directorios base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.join(BASE_DIR, 'site')
STATIC_ROOT = os.path.join(BASE_DIR, 'home/static')

# Rutas principales
urlpatterns = [
    # Raíz del sitio
    path('', HomeView.as_view(), name='home'),

    # Administración de Django
    path('admin/', admin.site.urls),

    # Autenticación y autorización
    path('authz/', include('authz.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Rutas estándar de autenticación
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),  # Autenticación social

    # Aplicaciones del proyecto
    path('api_xm/', include('api_xm.urls', namespace='api_xm')),

    # Contenido estático del directorio 'site'
    re_path(r'^site/(?P<path>.*)$', serve, {
        'document_root': SITE_ROOT,
        'show_indexes': True
    }, name='site_path'),

    # Favicon
    path('favicon.ico', serve, {
        'path': 'favicon.ico',
        'document_root': STATIC_ROOT
    }, name='favicon'),
]

# Configuración de login social (si aplica)
try:
    from . import github_settings
    SOCIAL_LOGIN_TEMPLATE = 'registration/login_social.html'
    urlpatterns.insert(0, path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name=SOCIAL_LOGIN_TEMPLATE),
        name='login'
    ))
    print(f"Usando {SOCIAL_LOGIN_TEMPLATE} como plantilla de login")
except ImportError:
    print("Usando 'registration/login.html' como plantilla de login por defecto")

# Servir archivos estáticos en modo DEBUG
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)