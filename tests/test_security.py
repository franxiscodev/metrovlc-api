"""
Test de password y JWT

ejecutar desde raiz
python -m tests.test_security
"""

from app.core.security import get_pwd_hash
from app.core.security import verify_pwd


def test_password_hashing():
    print("TEST DE HASHING DE PASSWORD")

    password = "super_agente_86"
    hashed = get_pwd_hash(password)

    print(f"-Contraseña original: {password}")
    print(f"-Hash generado: {hashed[:20]}...")
    print("\n")
    print("-"*50)

    is_valid = verify_pwd(password, hashed)
    print(f"-Password: {password}")
    print(f"-Resultado: {'Verificada ok' if is_valid else 'Inválida'}")


"""
falta el test del JWT, pero quiero avanzar con otros temas
"""


def test_jwt_tokens():
    pass


if __name__ == "__main__":
    try:
        test_password_hashing()
        print(f"\n test OK! \n")
    except Exception as e:
        print(f"\n Error del test KO: {e}\n")
        raise
