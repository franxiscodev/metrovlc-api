"""
Test de endpoints de la API usando requests.
El servidor debe estar corriendo en http://localhost:8000
uvicorn app.main:app --reload
luego ejecutar
python -m tests.test_endpoints
"""
import requests
import json
from app.core.config import settings

print(f"BASE_URL: {settings.BASE_URL}")
print(f"DATABASE_URL: {settings.DATABASE_URL}")
print(f"TEST_USERNAME: {settings.TEST_USERNAME}")
print(f"TEST_EMAIL: {settings.TEST_EMAIL}")
print(f"TEST_PASSWORD: {settings.TEST_PASSWORD}")


def print_section(title):
    """Imprime una sección con onda"""
    print("\n" + ". "*50)
    print(f"  {title}")
    print(". "*50)


def print_response(title, response):
    """Imprime la respuesta con onda"""
    print(f"\n{title}")
    print(f"Status Code: {response.status_code}")
    print("Response:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)


def test_register():
    """01: Registrar un nuevo usuario"""
    print_section("01: REGISTRO DE USUARIO")

    url = f"{settings.BASE_URL}/register"
    data = {
        "username": settings.TEST_USERNAME,
        "email": settings.TEST_EMAIL,
        "pwd": settings.TEST_PASSWORD
    }

    print(f"POST {url}")
    print(
        f"Datos: username={settings.TEST_USERNAME}, email={settings.TEST_EMAIL}")

    response = requests.post(url, json=data)
    print_response("Respuesta:", response)

    if response.status_code == 201:
        print("OK: Usuario registrado correctamente")
        return True
    else:
        print("KO: Error al registrar usuario")
        return False


def test_login():
    """02: Iniciar sesión y obtener token"""
    print_section("02: LOGIN DE USUARIO")
    url = f"{settings.BASE_URL}/login"
    data = {
        "username": settings.TEST_USERNAME,
        "pwd": settings.TEST_PASSWORD
    }

    print(f"POST {url}")
    print(f"Datos: username={settings.TEST_USERNAME}")

    response = requests.post(url, json=data)
    print_response("Respuesta:", response)

    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"OK: Login exitoso")
        print(f"Token: {token[:50]}...")
        return token
    else:
        print("KO: Error al hacer login")
        return None


def test_search_stations(token):
    """04: Buscar estaciones"""
    print_section("04: BUSCAR ESTACIONES")

    # Test 4.1: Buscar "colon"
    print("\n Búsqueda 1: 'colon'")
    url = f"{settings.BASE_URL}/stations/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": "colon"}

    print(f"GET {url}?q=colon")

    response = requests.get(url, params=params, headers=headers)
    print_response("Respuesta:", response)

    station_id = None
    if response.status_code == 200:
        data = response.json()
        print(f"OK: Búsqueda exitosa")
        print(f"   Total resultados: {data['total']}")
        if data['total'] > 0:
            station = data['results'][0]
            station_id = station['id']
            print(
                f"   Primera estación: {station['nombre']} (ID: {station_id})")
    else:
        print("KO: Error en búsqueda")

    # Test 4.2: Buscar "ben"
    print("\n Búsqueda 2: 'ben'")
    params = {"q": "ben"}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"   Total resultados: {data['total']}")
        if data['total'] > 0:
            for station in data['results'][:3]:
                print(f"   - {station['nombre']}")

    return station_id


def run_all_tests():
    """
    Ejecuta todos los tests en orden
    del flujo completo de un usuario
    """
    print("\n" + "🚇 "*30)
    print("TESTS COMPLETOS DE LA API - METROVALENCIA")
    print("🚇 "*30)

    test_register()

    token = test_login()
    print(token)
    if not token:
        print("***** KO Tests cancelados por error en el login ******")
        return

    test_search_stations(token)

    # Fin de los test si llega aca esta todo ok
    print("Todos los test OK")


if __name__ == "__main__":
    run_all_tests()
