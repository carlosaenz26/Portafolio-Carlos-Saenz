
#api_xm/utils.py
import requests

def fetch_xm_data(endpoint, metric_id, start_date, end_date, entity, filters=None):
    base_url = "https://servapibi.xm.com.co/"
    url = f"{base_url}{endpoint}"
    payload = {
        "MetricId": metric_id,
        "StartDate": start_date,
        "EndDate": end_date,
        "Entity": entity,
        "Filter": filters if filters else []
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error al consumir el API en {endpoint}: {str(e)}")