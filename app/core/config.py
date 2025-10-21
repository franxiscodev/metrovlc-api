"""
Aquí va la config de toda la app
y la carga de las variables porque uso un archivo
.env
el cual no se sube a github, en su lugar subire un ejemplo orientativo
.env.example

doc: https://fastapi.tiangolo.com/es/advanced/settings/#crear-el-objeto-settings
"""
from pydantic_settings import BaseSettings
# configurar la Clase Setting de pydantic con  las variables de entorno a utilizar


class Settings(BaseSettings):
    # configuraciones generales del proyecto
    PROJECT_NAME: str = "Metrovalencia API"
    API_V1_PREFIX: str = "/api/v1"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API para gestionar la movilidad de usuarios de Metrovalencia"
    BASE_URL: str = "http://localhost:8000/api/v1"

    # Configuración de seguridad JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # la base de datos
    DATABASE_URL: str = "sqlite:///./metrovalencia.db"

    # la API externa que consulto horarios en tiempo real y un timeout para evitar bloqueo
    METRO_API_BASE_URL: str = "https://geoportal.valencia.es/geoportal-services/api/v1"
    METRO_API_TIMEOUT: int = 10

    # NUEVA API FGV la anterior es muy inestable
    FGV_API_BASE_URL: str = "https://www.fgv.es/ap18/api/public/es/api/v1/V/horarios-prevision-3"

    TEST_USERNAME: str = "test_user"
    TEST_EMAIL: str = "test_user@ejemplo.com"
    TEST_PASSWORD: str = "test123"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

"""
funcion para realizar pruebas de la configuracion
ver 
./tests/test_config.py
ejecutar
python -m tests.test_config.py
"""
