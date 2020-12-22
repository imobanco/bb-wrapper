import io
import base64
import logging

from barcode import generate
import unidecode


def generate_barcode_b64image(barcode_number, text=None):
    """
    Método para gerar uma imagem base46 a partir de um código de barras numérico.
    """
    buffer = io.BytesIO()
    generate(name="itf", code=barcode_number, output=buffer, text=text)
    base64_img = base64.b64encode(buffer.getvalue())
    return base64_img


def parse_unicode_to_ascii(string):
    """
    Método para transliterar um texto com caracteres especiais
    em um texto maiúsculo sem caracteres especiais.
    """
    ascii_string = unidecode.unidecode(string)
    return ascii_string.upper()


def _get_logger(name):
    """
    factory de Logger's

    Args:
        name: nome para gerar o logger

    Returns:
        novo logger para bb_wrapper.{name}
    """
    return logging.getLogger(f"bb_wrapper.{name}")

