from django.urls import path
from . import views

app_name = 'api_xm'

urlpatterns = [
    path('dashboard/', views.api_xm_dashboard, name='api_xm_dashboard'),
    #path('collections/', views.view_collections, name='collections'),
    #path('metric/<str:metric_id>/', views.view_metric_data, name='metric_data'),
]
# from django.urls import path
# from . import views

# app_name = 'api_xm'

# urlpatterns = [
#     path('dashboard/', views.api_xm_dashboard, name='api_xm_dashboard'),
# ]
