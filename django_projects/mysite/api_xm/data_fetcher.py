import pandas as pd
from pydataxm import pydataxm
import logging

# Configuración de logs
logging.basicConfig(
    filename='api_xm.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def list_available_collections():
    """Obtiene y retorna las colecciones disponibles de la API de XM.

    Conecta con la API de XM utilizando la librería pydataxm, recupera las colecciones
    disponibles y las devuelve en un DataFrame de pandas.

    Returns:
        pd.DataFrame: DataFrame con las colecciones disponibles.
    """
    try:
        logging.info("Iniciando conexión con la API de XM para obtener colecciones disponibles.")
        api_client = pydataxm.ReadDB()
        collections_df = api_client.get_collections()

        #print(f"🔍 Collections obtenidas: {collections_df}")  # <- Agregamos esta línea para depuración
        if collections_df is not None:
            # Convertimos el DataFrame a una lista de diccionarios
            grouped = collections_df.groupby(['Type', 'Entity']).apply(lambda df: df.to_dict(orient='records')).to_dict()
            print(f"🔍 Collections agrupadas: {list(grouped.keys())}")
            
            #collections_list = collections_df.to_dict(orient='records')
            #print(f"🔍 Collections obtenidas: {collections_list[:5]}")  # Solo mostramos las 5 primeras
            return grouped
        else:
            logging.warning("La API devolvió 'None', no hay colecciones disponibles.")
            return {}

    except Exception as e:
        logging.error(f"Error al conectar con la API de XM: {e}", exc_info=True)
        return pd.DataFrame()


def validar_dataframe(df: pd.DataFrame) -> bool:
    """Valida si un DataFrame no está vacío.

    Args:
        df (pd.DataFrame): El DataFrame a validar.

    Returns:
        bool: True si el DataFrame no está vacío, False de lo contrario.
    """
    try:
        return not df.empty
    except Exception as e:
        logging.error(f"Error al validar el DataFrame: {e}", exc_info=True)
        return False


def main():
    """Función principal para probar la conexión con la API de XM y listar las colecciones disponibles."""
    try:
        logging.info("Iniciando prueba de conexión con la API de XM...")
        collections = list_available_collections()

        if validar_dataframe(collections):
            logging.info("📊 Colecciones disponibles:")
            logging.info(collections[['MetricId', 'MetricName', 'Url']])
            print("✅ Colecciones disponibles obtenidas. Consulte el archivo api_xm.log para más detalles.")
        else:
            logging.warning("⚠️ No se encontraron colecciones disponibles o hubo un error en la conexión.")

    except Exception as e:
        logging.critical(f"Error crítico al ejecutar el proceso principal: {e}", exc_info=True)


if __name__ == "__main__":
    main()
