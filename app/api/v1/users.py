"""
Endpoints de usuario (JWT): perfil, favoritos y llegadas.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserMeResponse, UserResponse
from app.schemas.station import (
    AddFavoriteResponse,
    FavoriteStationsResponse,
    StationSimple,
    DeparturesResponse
)
from app.services.station_service import (
    add_favorite_station,
    remove_favorite_station,
    get_user_favorite_stations,
    get_station_by_id
)
from app.services.external_api_service import (
    get_multiple_stations_departures,
    format_departures_response
)
from app.core.config import settings

router = APIRouter()


@router.get("/me", response_model=UserMeResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    favorites_count = len(current_user.favorite_stations)

    response = {
        "user": current_user,
        "fav_stations_count": favorites_count,
        "links": {
            "self": f"{settings.API_V1_PREFIX}/users/me",
            "favorites": f"{settings.API_V1_PREFIX}/users/me/stations",
            "add_favorite": f"{settings.API_V1_PREFIX}/users/me/stations/{{station_id}}",
            "departures": f"{settings.API_V1_PREFIX}/users/me/departures",
            "search_station": f"{settings.API_V1_PREFIX}/users/me/search=?q="
        }
    }

    return response


@router.get("/me/stations", response_model=FavoriteStationsResponse)
async def get_my_favorite_stations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    favorites = get_user_favorite_stations(db, current_user)

    response = {
        "favorites": favorites,
        "total": len(favorites),
        "links": {
            "self": f"{settings.API_V1_PREFIX}/users/me/stations",
            "departures": f"{settings.API_V1_PREFIX}/users/me/departures",
            "search": f"{settings.API_V1_PREFIX}/stations/search?q=",
        }
    }

    return response


@router.post("/me/stations/{station_id}", response_model=AddFavoriteResponse,
             status_code=status.HTTP_201_CREATED)
async def add_station_to_favorites(
    station_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        station = add_favorite_station(db, current_user, station_id)
        favorites_count = len(current_user.favorite_stations)
        response = {
            "message": "Estación agregada OK en favs",
            "station": station,
            "total_favorites": favorites_count
        }
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al agregar estación a favs: {str(e)}"
        )


@router.delete("/me/stations/{station_id}")
async def remove_station_favorites(
    station_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        station = remove_favorite_station(db, current_user, station_id)
        favorites_count = len(current_user.favorite_stations)

        return {
            "message": "Estación eliminada de favs",
            "station": {
                "id": station.id,
                "nombre": station.nombre,
                "codigo": station.codigo,
                "linea": station.linea
            },
            "total_favorites": favorites_count
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detal=f"Error al querer eliminar una estacion de favs {str(e)}"
        )


@router.get("/me/departures", response_model=DeparturesResponse)
async def get_my_departures(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    favorites = get_user_favorite_stations(db, current_user)

    if not favorites:
        return {
            "departures": [],
            "total_stations": 0,
            "timestamp": ""
        }

    try:
        stations_data = get_multiple_stations_departures(favorites)

        response = format_departures_response(stations_data)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error consultando llegadas: {str(e)}"
        )
