"""
Dependencias de FastAPI
Depends -> auto-gestionada por FastAPI
para no generar codigo repetitivo en cada endpoint
Sesión BD 
User autenticado
"""
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import verify_token
from app.models import User

# Configurar seguridad Bearer
security = HTTPBearer()

# cnx DB


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                           db: Session = Depends(get_db)) -> User:
    token = credentials.credentials  # obtener el token del header

    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no valido o expiró",
            headers={
                "WWW-Authenticate": "Bearer",
                "X-Error-Message": "Token no valido o expiró"
            }
        )

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={
                "WWW-Authenticate": "Bearer",
                "X-Error-Message": "Usuario no encontrado"
            }
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    return user
