import io
import base64
import logging
import re

from barcode import generate
import unidecode


def generate_barcode_b64image(barcode_number, text=None):
    """
    Método para gerar uma imagem base46 a partir de um código de barras numérico.
    """
    buffer = io.BytesIO()
    generate(name="itf", code=barcode_number, output=buffer, text=text)
    base64_img = base64.b64encode(buffer.getvalue())
    return base64_img.decode("utf-8")


def parse_unicode_to_alphanumeric(string):
    """
    Método para transliterar um texto com caracteres especiais
    em um texto maiúsculo sem caracteres especiais.
    """
    ascii_string = unidecode.unidecode(string)
    alphanumeric_string = re.sub(r"[^A-Za-z0-9]", "", ascii_string)
    return alphanumeric_string.upper()


def _get_logger(name):
    """
    factory de Logger's

    Args:
        name: nome para gerar o logger

    Returns:
        novo logger para bb_wrapper.{name}
    """
    return logging.getLogger(f"bb_wrapper.{name}")
