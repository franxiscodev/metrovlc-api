"""
Inicializar DB
    crear tablas
    importar CSV
ejecutar
    python init_database.py
"""

from app.core.database import engine, SessionLocal, Base
from app.models.user import User
from app.models.station import Station
from app.utils.text_normalize import normalize_text


def create_tables():
    print("-"*50)
    print("CREANDO TABLAS")
    print("-"*50)

    Base.metadata.create_all(bind=engine)

    print("OK tables")


def load_stations_from_csv():
    print("-"*50)
    print("CARGANDO LAS ESTACIONES DEL CSV")
    print("-"*50)

    print("OK tables")
