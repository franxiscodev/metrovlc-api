"""
eliminar tildes
eliminar funny characters ;)
todo a min
espacios en blancos innecesarios
"""

from unidecode import unidecode


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text_not_accents = unidecode(text)

    text_lower = text_not_accents.lower()

    text_ok = " ".join(text_lower.split())

    return text_ok
