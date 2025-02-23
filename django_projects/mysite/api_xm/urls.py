from django.urls import path
from .views import get_collections_tree, dashboard_view
from .views import dashboard_view, xm_dashboard_data
app_name = "api_xm"

urlpatterns = [
    path('dashboard/', dashboard_view, name='api_xm_dashboard'),
    path("dashboard/data/", xm_dashboard_data, name="xm_dashboard_data"),
    path('collections-tree/', get_collections_tree, name='collections_tree'),  # <-- Nueva ruta
]
