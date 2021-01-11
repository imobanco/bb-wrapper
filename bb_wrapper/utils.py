import io
import base64
import logging
import re

from barcode import generate as generate_barcode
from barcode.writer import SVGWriter
from qrcode import make as generate_qrcode
from qrcode.image.svg import SvgImage
import unidecode


def _generate_b64image_from_buffer(buffer, data_uri_schema="data:image/svg+xml;base64"):
    base64_img = base64.b64encode(buffer.getvalue())
    base64_string = f"{data_uri_schema},{base64_img.decode('utf-8')}"
    return base64_string


def generate_barcode_b64image(barcode_number, text=""):
    """
    Método para gerar uma imagem base46 a partir de um código de barras numérico.
    """
    buffer = io.BytesIO()
    generate_barcode(
        name="itf", code=barcode_number, output=buffer, text=text, writer=SVGWriter()
    )
    return _generate_b64image_from_buffer(buffer)


def generate_qrcode_b64image(qrcode_data):
    buffer = io.BytesIO()
    qrcode = generate_qrcode(qrcode_data, image_factory=SvgImage)
    qrcode.save(buffer)
    return _generate_b64image_from_buffer(buffer)


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
