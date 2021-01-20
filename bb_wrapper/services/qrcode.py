import io

from qrcode import make as generate_qrcode
from qrcode.image.svg import SvgImage

from .b64 import Base64Service


class QRCodeService:
    def generate_qrcode_b64image(self, qrcode_data):
        """
        Método para gerar uma imagem base64 a partir de um qrcode data.
        """
        buffer = io.BytesIO()
        qrcode = generate_qrcode(qrcode_data, image_factory=SvgImage)
        qrcode.save(buffer)
        return Base64Service().generate_b64image_from_buffer(buffer)
