import logging
from typing import List, Dict, Any, Tuple
import pandas as pd
from pydataxm import *  # Importamos todo como en tu prueba funcional

logger = logging.getLogger(__name__)

def get_collections_df() -> pd.DataFrame:
    """
    Retorna el DataFrame crudo con las colecciones disponibles en la API XM.
    """
    logger.info("Obteniendo DataFrame de colecciones desde la API XM")
    api_client = pydataxm.ReadDB()
    df = api_client.get_collections()

    if df is None or df.empty:
        logger.warning("La API devolvió DF vacío o None al solicitar colecciones.")
        return pd.DataFrame()  # DF vacío

    logger.debug(f"DF crudo: {df.head().to_dict()}")
    return df


def group_collections(collections_df: pd.DataFrame) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """
    Devuelve un dict con la estructura:
    {
      'HourlyEntities': {
        'Sistema': [
          { 'MetricId': 'DemaReal', 'MetricName': '...', ... },
          { 'MetricId': 'Gene', 'MetricName': '...', ... }
        ],
        'Agente': [...],
        ...
      },
      'DailyEntities': {
        'Sistema': [...],
        ...
      },
      ...
    }
    """
    # Primero filtra filas con Type, Entity y MetricId no vacíos
    df = collections_df.dropna(subset=["Type", "Entity", "MetricId"])
    if df.empty:
        logger.warning("Tras filtrar, no quedaron filas con Type, Entity y MetricId válidos.")
        return {}

    grouped = df.groupby(["Type", "Entity"]).apply(lambda subdf: subdf.to_dict(orient="records")).to_dict()

    final_data = {}
    for (type_val, entity_val), records in grouped.items():
        if type_val not in final_data:
            final_data[type_val] = {}
        final_data[type_val][entity_val] = records

    logger.info(f"Estructura jerárquica: {list(final_data.keys())} top-level Types.")
    return final_data


def list_available_collections() -> List[Tuple[str, str, List[Dict[str, Any]]]]:
    """
    Retorna una lista de tuplas (type_, entity, metrics)
    para quienes prefieran usar esa estructura.
    """
    try:
        df = get_collections_df()
        if df.empty:
            return []

        # Agrupamos en un dict con clave (Type, Entity)
        enriched_collections = {}
        for record in df.to_dict(orient='records'):
            type_ = record.get('Type', 'Unknown')
            entity = record.get('Entity', 'Unknown')
            key = (type_, entity)
            if key not in enriched_collections:
                enriched_collections[key] = []
            enriched_collections[key].append(record)

        # Convertimos a lista de tuplas
        result = [(t, e, metrics) for (t, e), metrics in enriched_collections.items()]
        logger.info(f"Colecciones en formato de tuplas: {[(t,e) for t,e,_ in result][:10]} ...")
        return result
    except Exception as e:
        logger.error(f"Error en list_available_collections: {e}", exc_info=True)
        return []


def fetch_metric_data(metric_id: str, start_date: str, end_date: str) -> Dict[str, Any]:
    """
    Obtiene datos específicos de una métrica desde la API de XM para un rango de fechas.
    """
    try:
        logger.info(f"Consultando datos para {metric_id} desde {start_date} hasta {end_date}")
        api_client = pydataxm.ReadDB()
        
        # Obtener datos de la métrica (dependiendo de la API pydataxm real)
        data_df = api_client.request_data(metric_id, start_date, end_date)
        if data_df is None or data_df.empty:
            logger.warning(f"No se encontraron datos para {metric_id} en el rango {start_date} - {end_date}")
            return {"Values": [], "metric_id": metric_id, "status": "no_data"}
        
        data = {"Values": data_df.to_dict(orient="records"), "metric_id": metric_id, "status": "success"}
        logger.debug(f"Datos obtenidos: {data['Values'][:5]}")
        return data
    except AttributeError as e:
        logger.error(f"Error en la API pydataxm (posible cambio de interfaz): {e}", exc_info=True)
        return {"error": str(e), "metric_id": metric_id, "status": "error"}
    except Exception as e:
        logger.error(f"Error general al obtener datos para {metric_id}: {e}", exc_info=True)
        return {"error": str(e), "metric_id": metric_id, "status": "error"}


def main() -> None:
    """
    Prueba local del módulo.
    """
    try:
        logger.info("Iniciando prueba del módulo data_fetcher")
        df = get_collections_df()
        print(f"DF shape: {df.shape}")
        grouped = group_collections(df)
        print(f"Keys top-level: {list(grouped.keys())[:5]} ...")

        # Prueba del list_available_collections
        list_collections = list_available_collections()
        print(f"Colecciones en list: {len(list_collections)} grupos.")

        # Prueba de fetch_metric_data con algo ficticio
        sample = fetch_metric_data("DemaReal", "2025-01-01", "2025-02-01")
        print(f"Resultado metric data: {sample['status']} con {len(sample.get('Values',[]))} filas.")
    except Exception as e:
        logger.critical(f"Error crítico en la prueba: {e}", exc_info=True)
        print(f"❌ Error en la prueba: {e}")


if __name__ == "__main__":
    main()
