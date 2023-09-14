import io

from qrcode import make as generate_qrcode
from qrcode.image.svg import SvgImage
from qrcode.image.pil import PilImage

from .b64 import Base64Service


class QRCodeService:
    def __init__(self):
        self.svg_factory = SvgImage
        self.png_factory = PilImage

        self.factory_mapping = {"png": PilImage, "svg": SvgImage}

    def generate_qrcode_b64image(self, qrcode_data, image_type="png"):
        """
        Método para gerar uma imagem base64 a partir de um qrcode data.
        """
        factory = self.factory_mapping[image_type]

        buffer = io.BytesIO()
        qrcode = generate_qrcode(qrcode_data, image_factory=factory)
        qrcode.save(buffer)

        return Base64Service().generate_b64image_string_from_buffer(
            buffer, image_type=image_type
        )
