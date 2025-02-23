import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .data_fetcher import list_available_collections, fetch_metric_data
import pandas as pd
from datetime import datetime
import plotly.express as px
from django.template.loader import render_to_string

# Configura logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@login_required
def api_xm_dashboard(request):
    """
    Vista para el dashboard principal de la API XM.
    Muestra una tabla con todas las métricas disponibles y botones para consultar datos.
    """
    try:
        logger.debug("Iniciando api_xm_dashboard")
        collections = list_available_collections() or []  # Lista de tuplas de longitud variable
        logger.info(f"Collections obtenidas: {collections[:5]}")  # Muestra primeros 5 para depuración
        
        context = {"collections": collections}
        logger.info("Intentando renderizar api_xm/collections.html")
        logger.info(f"Estructura de collections: {[tuple(c) for c in collections[:2]]}")
        return render(request, "api_xm/collections.html", context)
    
    except Exception as e:
        logger.error(f"Error en api_xm_dashboard: {str(e)}", exc_info=True)
        return render(request, "api_xm/error.html", {"error": str(e)}, status=500)

@login_required
def metric_data_view(request, metric_id):
    """Vista para formulario de fechas."""
    try:
        logger.info(f"Cargando formulario para métrica: {metric_id}")
        return render(request, "api_xm/metric_data.html", {"metric_id": metric_id})
    except Exception as e:
        logger.error(f"Error en metric_data_view: {str(e)}", exc_info=True)
        return render(request, "api_xm/error.html", {"error": str(e)}, status=500)

@login_required
def fetch_metric_data_view(request, metric_id):
    """Vista para obtener datos y generar gráficas."""
    try:
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if not start_date or not end_date:
            return JsonResponse({"error": "Debe ingresar fechas de inicio y fin"}, status=400)

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            if start > end:
                return JsonResponse({"error": "La fecha de inicio debe ser anterior a la de fin"}, status=400)
        except ValueError:
            return JsonResponse({"error": "Formato de fecha inválido (YYYY-MM-DD)"}, status=400)

        data = fetch_metric_data(metric_id, start_date, end_date)
        if not data or "Values" not in data or not data["Values"]:
            return JsonResponse({"error": "No se encontraron datos para esta métrica"}, status=404)

        df = pd.DataFrame(data["Values"])
        fig = px.line(df, x="Date", y="Value", title=f"Datos de {metric_id}")
        graph_html = fig.to_html(full_html=False)

        context = {"metric_id": metric_id, "graph_html": graph_html, "start_date": start_date, "end_date": end_date}
        html_content = render_to_string("api_xm/metric_graph.html", context)
        return JsonResponse({"html": html_content})

    except Exception as e:
        logger.error(f"Error en fetch_metric_data_view: {str(e)}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)