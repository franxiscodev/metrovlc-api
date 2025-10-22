"""
Endpoints de estaciones (JWT) búsqueda, filtrado y listado.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_db, get_current_user
from app.models import User
from app.schemas.station import (
    StationSimple,
    StationResponse,
    StationSearchResponse
)
from app.services.station_service import (
    search_stations,
    get_stations_by_line,
    get_station_by_id,
    get_all_lines
)
from app.core.config import settings

router = APIRouter()


@router.get("/search", response_model=StationSearchResponse)
async def search_by_stations(
        q: str = Query(..., min_length=3,
                       description="Nombre estación a buscar (min 3 caracteres"),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    try:
        results = search_stations(db, q, limit=5)
        response = {
            "results": results,
            "total": len(results),
            "query": q,
            "links": {
                "self": f"{settings.API_V1_PREFIX}/stations/search?q={q}",
                "add_favorite": f"{settings.API_V1_PREFIX}/users/me/stations/{{station_id}}",
                "my_favorites": f"{settings.API_V1_PREFIX}/users/me/stations"
            }
        }
        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar estaciones con texto: {str(e)}"
        )


@router.get("/", response_model=List[StationSimple])
async def list_stations(
    linea: str | None = Query(
        None, description="Filtrar por línea (L1, L2, L3 ... L10)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Listar estaciones con filtros opcionales.
    Sin query param trae todas las estaciones del metro

    /api/v1/stations/?linea=L3
    """
    try:
        if linea:
            # Filtrar por línea
            stations = get_stations_by_line(db, linea)
        else:
            # Listar todas las estaciones
            from app.models import Station
            stations = db.query(Station).order_by(Station.nombre).all()

        return stations

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar estaciones: {str(e)}"
        )


@router.get("/lines", response_model=List[str])
async def list_lines(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        lines = get_all_lines(db)
        return lines

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener líneas: {str(e)}"
        )


@router.get("/{station_id}", response_model=StationResponse)
async def get_station_detail(
    station_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        station = get_station_by_id(db, station_id)
        return station

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estación: {str(e)}"
        )
