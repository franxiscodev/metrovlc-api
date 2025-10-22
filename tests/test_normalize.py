"""

ejecutar
python -m tests.test_normalize
"""

from app.utils.text_normalize import normalize_text


def test_normalize():
    print("TEST DE NORMALIZAR TEXTO")

    texto = " Àngel Guimerà "

    texto_normalizado = normalize_text(texto)

    print(f"-Texto original:{texto}...")
    print(f"-Texto normalizado:{texto_normalizado}...")
    print("\n")
    print("-"*50)


if __name__ == "__main__":
    test_normalize()
