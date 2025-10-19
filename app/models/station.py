from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
# la Base declarativa
from app.core.database import Base
# el modelo de User para las relaciones con las estaciones
from app.models.user import user_favorite_stations


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    gid = Column(Integer, nullable=False, index=True)
    # codigo: Código de la estación (usado para API externa)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    # Nombre sin tildes y en minúsculas (para búsquedas)
    nombre_normalizado = Column(String(200), nullable=False, index=True)
    linea = Column(String(100), nullable=False, index=True)
    # no se va a usar, pero lo guardo para escalar a futuro
    geo_point_2d = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # definir las relaciones con los usuarios
    favorited_by = relationship(
        "User",
        secondary=user_favorite_stations,
        back_populates="favorite_stations"
    )
