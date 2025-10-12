"""
Autenticacion y Autorizacion
para puntos extras ;)

funciones de seguridad
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
# leer configuraciones privada de las variables de entorno
from app.core.config import settings

# para hashear las passwords, el algoritmo bcrypt parece ser el standadr
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# generar un hash con el algoritmo de pwd_context que se guara en la db
def get_pwd_hash(pwd: str) -> str:
    return pwd_context.hash(pwd)


# verificar si el password enviado coincide con su hash
def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)


# crear el token de acceso JWT
def create_acces_token(data: dict) -> str:
    to_encode = data.copy()

    # uso de las variables de entorno
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


# decodificar y validar token
def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


# verificar el token y extraer el usuario
def verify_token(token: str) -> Optional[str]:
    payload = decode_access_token(token)
    if payload is None:
        return None

    username: str = payload.get("sub")

    return username
