import logging
from data_fetcher import list_available_collections

# Configuración del registro de logs
logging.basicConfig(
    filename='api_xm.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Función principal para conectar con la API de XM y listar las colecciones disponibles."""
    logging.info("🔍 Iniciando prueba de conexión con la API de XM...")
    try:
        collections = list_available_collections()
        if collections is not None and not collections.empty:
            logging.info("✅ Conexión exitosa y colecciones obtenidas.")
            print("✅ Conexión exitosa y colecciones obtenidas.")
        else:
            logging.warning("⚠️ No se pudo obtener las colecciones o el DataFrame está vacío.")
            print("⚠️ No se pudo obtener las colecciones o el DataFrame está vacío.")
    except Exception as e:
        logging.error(f"❌ Error durante la conexión con la API de XM: {e}", exc_info=True)
        print("❌ Error al conectar con la API de XM. Consulte el log para más detalles.")

if __name__ == "__main__":
    main()