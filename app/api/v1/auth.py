"""
Endpoints de autenticación: registro y login.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.user import UserRegister, UserLogin, Token, UserResponse
from app.services.auth_service import register_user, login_user


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    try:
        new_user = register_user(db, user_data)
        return new_user
    except HTTPException:
        # Re-lanzar excepciones HTTP del servicio
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar el usuario {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        token_data = login_user(db, login_data)
        return token_data
    except HTTPException:
        # Re-lanzar excepciones HTTP del servicio
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al iniciar sesión: {str(e)}"
        )
