import io
import base64

from barcode import ITF


def generate_barcode_b64image(barcode_number):
    barcode_generator = ITF(barcode_number)
    buffer = io.BytesIO()
    barcode_generator.write(buffer)
    base64_img = base64.b64encode(buffer.getvalue())
    return base64_img
