"""
estructura de los datos de station
request - response
"""


from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class StationBase(BaseModel):
    codigo: str
    nombre: str
    linea: str


class StationResponse(StationBase):
    id: int
    gid: int
    nombre_normalizado: str
    geo_point_2d: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StationSimple(BaseModel):
    """
    para listados
    """
    id: int
    codigo: str
    nombre: str
    linea: str

    model_config = ConfigDict(from_attributes=True)

 # búsquedas


class StationSearchResponse(BaseModel):
    """
    respuesta de búsqueda de estaciones
    """
    results: List[StationSimple]
    total: int
    query: str
    links: dict


# llegadas de coches
class ArrivalInfo(BaseModel):
    linea: str | None = None
    destino: str | None = None
    tiempo: str | None = None
    tipo: str | None = None


class StationDepartures(BaseModel):
    """
    Schema para llegadas de una estación.
    """
    station_id: int
    station_name: str
    station_code: str
    arrivals: List[ArrivalInfo]
    has_data: bool
    message: str | None = None


class DeparturesResponse(BaseModel):
    """
    Schema para respuesta completa de llegadas de todas las estaciones favoritas.
    """
    departures: List[StationDepartures]
    total_stations: int
    timestamp: str


# Fsavoritos
class AddFavoriteResponse(BaseModel):
    """
    respuesta al añadir estación a favoritos
    """
    message: str
    station: StationSimple
    total_favorites: int


class FavoriteStationsResponse(BaseModel):
    """
    listar estaciones favoritas de un usuario
    """
    favorites: List[StationSimple]
    total: int
    links: dict
