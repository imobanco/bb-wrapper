import io

from qrcode import make as generate_qrcode
from qrcode.image.svg import SvgImage
from qrcode.image.pil import PilImage

from .b64 import Base64Service


class QRCodeService:
    SVG_FACTORY = SvgImage
    PNG_FACTORY = PilImage
    FACTORY_MAPPING = {"png": PNG_FACTORY, "svg": SVG_FACTORY}

    def _generate_qrcode_image_bytes(self, qrcode_data, image_type="png"):
        """
        Método para gerar os bytes da imagem a partir de um qrcode data.
        """
        factory = self.FACTORY_MAPPING[image_type]

        buffer = io.BytesIO()
        qrcode = generate_qrcode(qrcode_data, image_factory=factory)
        qrcode.save(buffer)
        return buffer.getvalue()

    def generate_qrcode_b64image(self, qrcode_data, image_type="png"):
        """
        Método para gerar uma imagem base64 a partir de um qrcode data.
        """
        image_bytes = self._generate_qrcode_image_bytes(
            qrcode_data=qrcode_data, image_type=image_type
        )
        return Base64Service().generate_b64image_string(
            image_bytes, image_type=image_type
        )
