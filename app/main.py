"""
Aplicación principal de FastAPI (versión temporal).
"""
from fastapi import FastAPI
from app.api.v1 import auth
from app.core.config import settings

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Incluir routers
app.include_router(
    auth.router, prefix=f"{settings.API_V1_PREFIX}", tags=["Autenticación"])
