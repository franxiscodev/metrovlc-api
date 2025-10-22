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
    url = f"{settings.FGV_API_BASE_URL}/{station_code}"
    # url = f"https://www.fgv.es/ap18/api/public/es/api/v1/V/horarios-prevision-3/{station_code}"

    print("🔍 DEBUG URL Para verificar")  # ← Para verificar
    print(f"🔍 DEBUG URL: {url}")  # ← Para verificar
    print("🔍 DEBUG URL Para verificar")  # ← Para verificar
    try:
        response = requests.get(
            url,
            timeout=settings.METRO_API_TIMEOUT
        )
        response.raise_for_status()

        data = response.json()

        if not data or not data.get("previsiones"):
            return {
                "has_data": False,
                "arrivals": [],
                "message": "No hay información disponible en este momento"
            }

        arrivals = []
        lineas_procesadas = set()  # Para evitar duplicados

        # Recorrer cada línea en previsiones
        for linea_info in data.get("previsiones", []):
            linea_numero = linea_info.get("line")
            linea_id = linea_info.get("linea_id_interna")

            # Procesar cada tren en la línea
            for tren in linea_info.get("trains", []):
                destino = tren.get("destino", "")
                segundos = tren.get("seconds", 0)

                # Filtrar datos no válidos
                if (segundos is not None and segundos > 0 and
                        destino and destino.strip()):

                    # Calcular minutos (redondeado)
                    minutos = max(1, round(segundos / 60))

                    # Determinar estado basado en tiempo
                    if segundos <= 120:  # 2 minutos o menos
                        estado = "INMINENTE"
                    elif segundos <= 300:  # 5 minutos o menos
                        estado = "PRÓXIMO"
                    else:
                        estado = "EN RUTA"

                    # arreglar los caracteres que se imprimen mal en la salida de la API FGV (Mar?tim)
                    destino_sin_simbolos = destino.replace(
                        "?", "ó").replace("Ã³", "ó")

                    arrival = {
                        "linea": str(linea_numero),
                        "linea_id": str(linea_id),
                        # Corregir encoding
                        "destino": destino_sin_simbolos,
                        "tiempo_segundos": segundos,
                        "tiempo_minutos": minutos,
                        "estado": estado
                    }

                    arrivals.append(arrival)
                    lineas_procesadas.add(str(linea_numero))

        # Ordenar por tiempo de llegada, más cercano primero
        arrivals.sort(key=lambda x: x["tiempo_segundos"])

        return {
            "has_data": len(arrivals) > 0,
            "arrivals": arrivals,
            "summary": {
                "total_llegadas": len(arrivals),
                "lineas_activas": list(lineas_procesadas),
                "proxima_llegada": arrivals[0] if arrivals else None,
                "estacion_codigo": station_code
            },
            "message": f"{len(arrivals)} llegadas encontradas" if arrivals else "No hay llegadas programadas"
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
        status_code = e.response.status_code if e.response else "N/A"
        return {
            "has_data": False,
            "arrivals": [],
            "message": f"Error HTTP {status_code}: El servicio no está disponible para la estación {station_code}"
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
            "message": departure_data.get("message"),
            "summary": departure_data.get("summary"),
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


"""

def get_station_departures_old(station_code: str) -> Dict:
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


"""
