# api_xm/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .utils import fetch_xm_data  # tu función que hace requests al API de XM
# api_xm/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .data_fetcher import get_collections_df  # tu función que obtiene el DF
from .data_fetcher import group_collections


@login_required
def get_collections_tree(request):
    """Retorna la estructura jerárquica Type->Entity->lista de métricas en JSON."""
    df = get_collections_df()  # supongamos que tienes algo así
    grouped_data = group_collections(df)
    return JsonResponse({"collections": grouped_data}, safe=False)

@login_required
def xm_dashboard_data(request):
    """Vista que recibe parámetros y devuelve datos en JSON, sin guardarlos en la BD."""
    endpoint = request.GET.get("endpoint")
    metric_id = request.GET.get("metric_id")
    entity = request.GET.get("entity")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filters = request.GET.getlist("filters", [])

    if not all([endpoint, metric_id, entity, start_date, end_date]):
        return JsonResponse({"error": "Faltan parámetros requeridos"}, status=400)

    try:
        data = fetch_xm_data(endpoint, metric_id, start_date, end_date, entity, filters)
        return JsonResponse({"data": data}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    """Renderiza el HTML con el dashboard sin guardar datos."""

    return render(request, 'api_xm/dashboard.html')

@login_required
def hourly_data(request):
    return xm_dashboard_data(request, endpoint='hourly')
