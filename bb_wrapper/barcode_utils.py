import io
import base64

from barcode import ITF
from barcode.writer import ImageWriter


def generate_barcode_b64image(barcode_number, filepath=None):
    barcode_generator = ITF(barcode_number, writer=ImageWriter())
    buffer = io.BytesIO()
    barcode_generator.write(buffer)
    base64_img = base64.b64encode(buffer.getvalue())
    if filepath is not None:
        with open(filepath, 'wb') as f:
            barcode_generator.write(f)
    return base64_img
