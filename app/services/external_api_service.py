"""
API Externa del Geoportal Valencia
consultar la información de llegadas en tiempo real
"""
import requests
from typing import List, Dict
from datetime import datetime
from app.core.config import settings
from app.models import Station


def get_station_departures(station_code: str) -> Dict:
    url = f"{settings.METRO_API_BASE_URL}/salidas-metro"
    params = {
        "estacion": station_code,
        "lang": "es"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=settings.METRO_API_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        if not data or (isinstance(data, dict) and not data.get("salidas")):
            return {
                "has_data": False,
                "arrivals": [],
                "message": "No hay info actualizada en este momento"
            }

        arrivals = []

        # distintas estructuras
        salidas = data.get("salidas", []) if isinstance(data, dict) else []

        for salida in salidas:
            arrival = {
                "linea": salida.get("linea", ""),
                "destino": salida.get("destino", ""),
                "tiempo": salida.get("tiempo", ""),
                "tipo": salida.get("tipo", "Metro")
            }
            arrivals.append(arrival)

        return {
            "has_data": True,
            "arrivals": arrivals
        }

    except requests.Timeout:
        return {
            "has_data": False,
            "arrivals": [],
            "message": f"Timeout: La API tardó más de {settings.METRO_API_TIMEOUT} segundos en responder"
        }

    except requests.ConnectionError:
        return {
            "has_data": False,
            "arrivals": [],
            "message": "Error de conexión: No se pudo conectar con el servicio de información"
        }

    except requests.HTTPError as e:
        return {
            "has_data": False,
            "arrivals": [],
            "message": f"Error HTTP {e.response.status_code}: El servicio no está disponible"
        }

    except requests.RequestException as e:
        return {
            "has_data": False,
            "arrivals": [],
            "message": f"Error en la petición: {str(e)}"
        }

    except Exception as e:
        return {
            "has_data": False,
            "arrivals": [],
            "message": f"Error inesperado: {str(e)}"
        }


def get_multiple_stations_departures(stations: List[Station]) -> List[Dict]:
    results = []

    for station in stations:
        departure_data = get_station_departures(station.codigo)
        result = {
            "station_id": station.id,
            "station_name": station.nombre,
            "station_code": station.codigo,
            "has_data": departure_data.get("has_data", False),
            "arrivals": departure_data.get("arrivals", []),
            "message": departure_data.get("message")
        }

        results.append(result)

    return results


def format_departures_response(stations_data: List[Dict]) -> Dict:

    return {
        "departures": stations_data,
        "total_stations": len(stations_data),
        "timestamp": datetime.utcnow().isoformat()
    }
