"""
Test de password y JWT
"""

from app.core.security import get_pwd_hash


def test_password_hashing():
    print("TEST DE HASHING DE PASSWORD")

    password = "super_agente_86"
    hashed = get_pwd_hash(password)

    print(f"-Contraseña original: {password}")
    print(f"-Hash generado: {hashed[:72]}...")
    print("\n")


if __name__ == "__main__":
    try:
        test_password_hashing()
        print(f"\n test OK! \n")
    except Exception as e:
        print(f"\n Error del test KO: {e}\n")
        raise
