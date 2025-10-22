"""
Aplicación principal de FastAPI - MetroValencia.
"""
from fastapi import FastAPI
from app.api.v1 import auth, stations, users
from app.core.config import settings

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION
)

# Endpoint raíz


@app.get("/")
async def root():
    return {
        "message": f"Bienvenido a {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "api": {
            "register": f"{settings.API_V1_PREFIX}/register",
            "login": f"{settings.API_V1_PREFIX}/login",
            "profile": f"{settings.API_V1_PREFIX}/users/me",
            "search_stations": f"{settings.API_V1_PREFIX}/stations/search?q="
        }
    }

# Incluir routers
app.include_router(
    auth.router, prefix=f"{settings.API_V1_PREFIX}", tags=["Autenticación"])
app.include_router(
    users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["Usuarios"])
app.include_router(
    stations.router, prefix=f"{settings.API_V1_PREFIX}/stations", tags=["Estaciones"])
