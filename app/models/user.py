from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
# la Base declarativa
from app.core.database import Base

# tabla de relaciones mucas a muchas entre los usuarios y sus estaciones favoritas
user_favorite_stations = Table(
    'user_favorite_stations',
    Base.metadata,
    Column('user_id', Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), primary_key=True),
    Column('station_id', Integer, ForeignKey(
        'stations.id', ondelete='CASCADE'), primary_key=True),
    Column('added_at', DateTime, server_default=func.now())
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_pwd = Column(String(255), nullable=False)
    # voy a  "desactivar" usuarios para no borrarlos
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # definir las relaciones con las estaciones
    favorite_stations = relationship(
        "Station",
        secondary=user_favorite_stations,
        back_populates="favorited_by"
    )
