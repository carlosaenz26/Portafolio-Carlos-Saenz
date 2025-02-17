import logging
from django.shortcuts import render
from .data_fetcher import list_available_collections
from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)
@login_required
def api_xm_dashboard(request):
    """Vista para mostrar el dashboard de la API XM."""
    try:
        collections = list_available_collections()
        if collections is None:
            logger.warning("La API devolvió 'None', no hay colecciones disponibles.")
            collections = []
        
        context = {'collections': collections}
        logger.info("API XM Dashboard cargado exitosamente.")
        return render(request, 'api_xm/collections.html', context)
    
    except Exception as e:
        logger.error(f"Error al cargar el dashboard de la API XM: {e}")
        return render(request, 'api_xm/error.html', {'error': str(e)})
