"""
Auth usuarios
Registro - Login - Validación
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User
from app.schemas.user import UserRegister, UserLogin
from app.core.security import get_pwd_hash, verify_pwd, create_acces_token


def get_user_by_name(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def get_user_by_mail(db: Session, mail: str) -> User:
    return db.query(User).filter(User.email == mail).first()


def register_user(db: Session, user_data: UserRegister) -> User:
    exist_user = get_user_by_name(db, user_data.username)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este husername ya está registado"
        )
    exist_mail = get_user_by_mail(db, user_data.email)
    if exist_mail:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este mail ya está registado"
        )

    # Hash de la pwd
    hashed_pwd = get_pwd_hash(user_data.pwd)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_pwd=hashed_pwd,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def autenticate_user(db: Session, login_data: UserLogin) -> User:
    user = get_user_by_name(db, login_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no válidas",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # verify_pwd = verify_pwd(login_data.pwd, user.hashed_pwd)
    if not verify_pwd(login_data.pwd, user.hashed_pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no válidas",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no activo"
        )

    return user


def login_user(db: Session, login_data: UserLogin) -> dict:
    user = autenticate_user(db, login_data)
    acces_token = create_acces_token(data={"sub": user.username})  # JWT Token
    return {
        "access_token": acces_token,
        "token_type": "bearer"
    }
