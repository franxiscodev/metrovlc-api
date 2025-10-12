"""
Configurar la DB sqlite y sqlalchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# importar el archivo de configuracion
from app.core.config import settings

# https://docs.sqlalchemy.org/en/14/core/engines.html#sqlalchemy.create_engine
# la opción echo sirve para cambiar entrre si queremos o no ver las queries SQL por terminal
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# la cnx en si misma
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear la DB y las tablas al inicializar la app
# , aun en proceso -> crear los modelos


def init_db():
    # from app.models import tablausuarios, tablaestaciones
    from app.models import user, station
    # create_all
    Base.metadata.create_all(bind=engine)
    print("base creada ok!")
