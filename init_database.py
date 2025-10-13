"""
Inicializar DB
    crear tablas
    importar CSV
ejecutar
    python init_database.py
"""

import os
import csv
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

    csv_path = "data/estaciones_metro.csv"
    if not os.path.exists(csv_path):
        print(
            f"Error no se encuentra el archivo CSV {csv_path} de las estaciones")

    db = SessionLocal()

    # leer el csv
    # problemas al cargar solo con utf-8 solución encontrada encoding='utf-8-sig'
    with open(csv_path, 'r', encoding='utf-8-sig') as file:

        reader = csv.DictReader(file, delimiter=';')
        print(f"Columnas disponibles: {reader.fieldnames}")

        for row in reader:
            station = Station(
                gid=int(row['gid']),
                codigo=row['Código'].strip(),
                nombre=row['Nombre'].strip(),
                nombre_normalizado=normalize_text(row['Nombre']),
                linea=row['Línea'].strip(),
                geo_point_2d=row['geo_point_2d'].strip()
            )
            db.add(station)

        db.commit()

    print("OK estaciones cargados")


def main():
    try:
        create_tables()
        load_stations_from_csv()
    except Exception as e:
        print(f"Error mientras inicializo: {e}")
        raise


if __name__ == "__main__":
    main()
