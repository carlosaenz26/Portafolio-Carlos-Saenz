# from django.urls import path
# from . import views
# from django.views.generic import TemplateView

# app_name='authz'
# urlpatterns = [
#     path('', TemplateView.as_view(template_name='authz/main.html')),
#     path('open', views.OpenView.as_view(), name='open'),
#     path('apereo', views.ApereoView.as_view(), name='apereo'),
#     path('manual', views.ManualProtect.as_view(), name='manual'),
#     path('protect', views.ProtectView.as_view(), name='protect'),
#     path('python', views.DumpPython.as_view(), name='python'),
# ]
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path
from .views import OpenView, ApereoView, ManualProtect, ProtectView, DumpPython, CustomLogoutView

app_name = 'authz'

urlpatterns = [
    path('', TemplateView.as_view(template_name='authz/main.html')),
    
    path('open', OpenView.as_view(), name='open'),
    path('apereo', ApereoView.as_view(), name='apereo'),
    path('manual', ManualProtect.as_view(), name='manual'),
    path('protect', ProtectView.as_view(), name='protect'),
    path('python', DumpPython.as_view(), name='python'),

    # Authentication views
    path('login/', auth_views.LoginView.as_view(template_name='authz/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Built-in Django LogoutView
    

]
