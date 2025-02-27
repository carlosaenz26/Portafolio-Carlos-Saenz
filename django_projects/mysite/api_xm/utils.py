import requests
import logging

# Configuración del logger
logging.basicConfig(
    filename='api_xm.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)
logger = logging.getLogger(__name__)

# Definir los endpoints correctos de la API XM
BASE_URL = "https://servapibi.xm.com.co/"
ENDPOINT_MAP = {
    "HourlyEntities": "hourly",
    "DailyEntities": "daily",
    "MonthlyEntities": "monthly",
    "ListsEntities": "list"
}

def fetch_xm_data(endpoint: str, metric_id: str, start_date: str, end_date: str, entity: str, filters=None):
    """
    Obtiene datos de la API de XM de manera segura y estructurada.

    Args:
        endpoint (str): Tipo de datos a consultar (HourlyEntities, DailyEntities, etc.).
        metric_id (str): Identificador de la métrica específica.
        start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'.
        end_date (str): Fecha de fin en formato 'YYYY-MM-DD'.
        entity (str): Entidad específica de la métrica.
        filters (list, optional): Filtros adicionales.

    Returns:
        dict: Respuesta JSON con los datos o un error estructurado.
    """
    if endpoint not in ENDPOINT_MAP:
        logger.error(f"❌ Endpoint no reconocido: {endpoint}")
        return {"error": f"Endpoint '{endpoint}' no válido"}

    url = f"{BASE_URL}{ENDPOINT_MAP[endpoint]}"
    payload = {
        "MetricId": metric_id,
        "StartDate": start_date,
        "EndDate": end_date,
        "Entity": entity,
        "Filter": filters if filters else []
    }

    logger.info(f"🔍 Solicitando datos a {url} con payload: {payload}")

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()  # Lanza error en caso de códigos 4XX/5XX

        data = response.json()
        if not data:
            logger.warning(f"⚠️ Respuesta vacía para {metric_id} en {url}")
            return {"error": "La API devolvió una respuesta vacía"}

        logger.info(f"✅ Datos obtenidos correctamente para {metric_id}")
        return data

    except requests.exceptions.Timeout:
        logger.error(f"⏳ Timeout al conectar con {url}")
        return {"error": "La solicitud a la API tardó demasiado y fue cancelada"}

    except requests.exceptions.ConnectionError:
        logger.error(f"🔌 Error de conexión con {url}")
        return {"error": "No se pudo conectar con la API de XM"}

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"❌ HTTP error {response.status_code}: {http_err}")
        return {"error": f"Error HTTP {response.status_code}: {http_err}"}

    except Exception as e:
        logger.error(f"❌ Error inesperado en fetch_xm_data: {e}")
        return {"error": f"Error inesperado: {str(e)}"}
