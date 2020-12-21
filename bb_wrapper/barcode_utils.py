import io
import base64

from barcode import generate


def generate_barcode_b64image(barcode_number, text=None):
    buffer = io.BytesIO()
    generate(name="itf", code=barcode_number, output=buffer, text=text)
    base64_img = base64.b64encode(buffer.getvalue())
    return base64_img
