"""
Estaciones
buscar - filtrar - favoritas
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from app.models import User, Station
from app.utils.text_normalize import normalize_text


def search_stations(db: Session, query: str, limit: int = 5) -> List[Station]:
    normalized_query = normalize_text(query)

    stations = db.query(Station).filter(
        Station.nombre_normalizado.contains(normalized_query)
    ).limit(limit).all()

    return stations


def get_stations_by_line(db: Session, line_id: str) -> List[Station]:
    stations = db.query(Station).filter(
        Station.linea == line_id).order_by(Station.nombre).all()
    return stations


def get_station_by_id(db: Session, station_id: int) -> Station:
    station = db.query(Station).filter(Station.id == station_id).first()
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"la estacion con ID {station_id} no se encuentra"
        )
    return station


def get_station_by_code(db: Session, station_code: str) -> Station:
    return de.query(Station).filter(Station.codigo == station_code).first()


def add_favorite_station(db: Session, user: User, station_id: int) -> Station:
    station = get_station_by_id(db, station_id)

    # ya esta en fav?
    if station in user.favorite_stations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta estacion ya esta en favoritos"
        )

    user.favorite_stations.append(station)
    db.commit()
    db.refresh(user)

    return station


def remove_favorite_station(db: Session, user: User, station_id: int) -> Station:
    station = get_station_by_id(db, station_id)
    if station not in user.favorite_stations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta estacion no esta en los favoritos"
        )

    user.favorite_stations.remove(station)
    db.commit()
    db.refresh(user)

    return station


def get_user_favorite_stations(db: Session, user: User) -> List[Station]:
    return user.favorite_stations


def get_all_lines(db: Session) -> List[str]:
    lines = db.query(Station.linea).distinct().order_by(Station.linea).all()
    return [line[0] for line in lines]
