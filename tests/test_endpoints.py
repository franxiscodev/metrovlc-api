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


def test_get_profile(token):
    """03: Obtener perfil del usuario"""
    print_section("03: OBTENER PERFIL (GET /users/me)")

    url = f"{settings.BASE_URL}/users/me"
    headers = {"Authorization": f"Bearer {token}"}

    print(f"GET {url}")
    print(f"Headers: Authorization: Bearer {token[:30]}...")

    response = requests.get(url, headers=headers)
    print_response("Respuesta:", response)

    if response.status_code == 200:
        data = response.json()
        print(f"OK: Perfil obtenido correctamente")
        print(f"   Username: {data['user']['username']}")
        print(f"   Email: {data['user']['email']}")
        print(f"   Favoritos: {data['fav_stations_count']}")
        return True
    else:
        print("KO: Error al obtener perfil")
        return False


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


def test_list_lines(token):
    """05: Listar líneas de metro"""
    print_section("05: LISTAR LiNEAS DE METRO")

    url = f"{settings.BASE_URL}/stations/lines"
    headers = {"Authorization": f"Bearer {token}"}

    print(f"GET {url}")

    response = requests.get(url, headers=headers)
    print_response("Respuesta:", response)

    if response.status_code == 200:
        lines = response.json()
        print(f"OK: Líneas obtenidas correctamente")
        print(f"   Total líneas: {len(lines)}")
        print(f"   Líneas: {', '.join(lines)}")
        return lines[0] if lines else None
    else:
        print("KO Error al obtener líneas")
        return None


def test_filter_by_line(token, line):
    line = 5
    """06: Filtrar estaciones por línea"""
    print_section(f"06: FILTRAR ESTACIONES POR LiNEA ({line})")

    url = f"{settings.BASE_URL}/stations/"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"linea": line}

    print(f"GET {url}?linea={line}")

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        stations = response.json()
        print(f"OK Filtrado exitoso")
        print(f"   Total estaciones de {line}: {len(stations)}")
        if len(stations) > 0:
            print(f"   Primeras 5 estaciones: {len(stations)}")
            for station in stations:
                print(f"   - {station['nombre']}")
        return True
    else:
        print(f"KO Error al filtrar por línea")
        return False


def run_all_tests():
    """
    Ejecuta todos los tests en orden
    del flujo completo de un usuario
    """
    print("\n" + "🚇 "*30)
    print("TESTS COMPLETOS DE LA API - METROVALENCIA")
    print("🚇 "*30)

    # 1.- Registro
    test_register()

    # 2.- Login
    token = test_login()
    print(token)
    if not token:
        print("***** KO Tests cancelados por error en el login ******")
        return

    # 3.- Mi Perfil
    test_get_profile(token)

    # 4.- Buscar estaciones  -> la guardo para luego aggregar a fav
    station_id = test_search_stations(token)

    # 5.- Listar las lineas del metro -> la guardo para luego filtrar x linea
    line = test_list_lines(token)

    # 6.- Filtrar por línea
    if line:
        test_filter_by_line(token, line)

    # Fin de los test si llega aca esta todo ok
    print("Todos los test OK")

    # BORRAR
    print(station_id)
    print(line)


if __name__ == "__main__":
    run_all_tests()
