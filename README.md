# Metrovalencia API 🚇

API REST para gestionar la movilidad de usuarios de Metrovalencia.

## 🎯 Características

- Gestión de usuarios con autenticación JWT
- Consulta de estaciones de metro
- Búsqueda flexible de estaciones (sin tildes, case-insensitive)
- Gestión de estaciones favoritas por usuario
- Consulta de llegadas en tiempo real desde API externa

## 🛠️ Tecnologías

- **Python 3.8+**
- **FastAPI**
- **SQLAlchemy**
- **JWT**
- **SQLite**

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/franxiscodev/metrovlc-api.git
cd metrovalencia-api
```

### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Renombrar archivo de ejemplo
cp .env.example .env

# IMPORTANTISIMO: Editar .env con una SECRET_KEY segura

```

### 5. Inicializar la base de datos

```bash
# Debe de estar el archivo CSV en data/estaciones_metro.csv
python init_database.py
```

---

## 🎯 Uso

### Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en:
- **API:** http://localhost:8000
- **Documentación Swagger:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

###  Ejecutar tests (en otra terminal) y veras un flujo completo del uso de la API

```bash
python -m tests.test_endpoints
```

## ⚙️ Configuración datos usuario de pruebas

### Archivo `/core/config.py`
```
TEST_USERNAME: str = "test_user"
TEST_EMAIL: str = "test_user@ejemplo.com"
TEST_PASSWORD: str = "test123"
```

## 📊 Flujo de Tests Automatizados

### El script `test_endpoints.py` ejecuta en orden:

- **Registro de usuario** - Crea un nuevo usuario de prueba
- **Login** - Obtiene token JWT de autenticación
- **Perfil de usuario** - Consulta información del usuario
- **Búsqueda de estaciones** - Busca estaciones por nombre
- **Listado de líneas** - Obtiene todas las líneas de metro
- **Filtrado por línea** - Filtra estaciones por línea específica
- **Añadir favoritos** - Agrega estación a favoritos del usuario
- **Listar favoritos** - Consulta estaciones favoritas
- **Consultar llegadas** - Obtiene llegadas en tiempo real de estaciones favoritas 😉🙌
- **Eliminar favoritos** - Elimina estación de favoritos


## 🙏 Agradecimientos

- **FastAPI** - Por el excelente framework
- **fgv.es Valencia** - Por proporcionar la API de datos del metro VLC
- **Pontia** - Por la formación integral
- **Alejandro** - Por las explicaciones y el empuje


