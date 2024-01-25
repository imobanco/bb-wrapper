import io
from typing import Union

from barcode import generate as generate_barcode
from barcode.writer import SVGWriter, ImageWriter

from pydantic import ValidationError

from .b64 import Base64Service
from ..models.barcode import BarcodeCobranca, BarcodeTributo
from bb_wrapper.services.barcode_cobranca import BarcodeCobrancaService
from bb_wrapper.services.barcode_tributo import BarcodeTributoService


class BarcodeService:
    SVG_WRITER = SVGWriter
    PNG_WRITER = ImageWriter
    WRITER_MAPPING = {"svg": SVG_WRITER, "png": PNG_WRITER}

    def _generate_barcode_image_bytes(
        self, barcode: str, include_number_in_image=True, image_type="png"
    ):
        if include_number_in_image:
            text = barcode
        else:
            text = ""

        writer = self.WRITER_MAPPING[image_type]()

        buffer = io.BytesIO()
        generate_barcode(
            name="itf",
            code=barcode,
            output=buffer,
            text=text,
            writer=writer,
            writer_options={
                "quiet_zone": 0,  # margin esquerda e direita (sem margem pois nosso template tem espaço!)  # noqa
                # "module_width": 0.3,  # largura (0.3 mm => 817px)
                "module_width": 0.2,  # largura (0.2 mm => 545px)
                # "module_width": 0.1,  # largura (0.2 mm => 272px)
                # "module_height": 14  # altura (14 mm => 60px)
                # "module_height": 13  # altura (13 mm => 56px)
                "module_height": 12,  # altura (12 mm => 52px)
            },
        )
        return buffer.getvalue()

    def generate_barcode_b64image(
        self, barcode: str, include_number_in_image=True, image_type="png"
    ) -> str:
        """
        Método para gerar uma imagem base46 a partir de um código de barras numérico.
        """
        image_bytes = self._generate_barcode_image_bytes(
            barcode,
            include_number_in_image=include_number_in_image,
            image_type=image_type,
        )
        return Base64Service().generate_b64image_string(
            image_bytes, image_type=image_type
        )

    def identify(self, number: str) -> Union[BarcodeCobranca, BarcodeTributo]:
        """
        Identifica e instância um Boleto Cobrança ou Boleto Tributo com base
        na linha digitável ou código de barras.

        Args:
            number: linha digitável ou código de barras

        Returns:
            Instância um Boleto Cobrança ou Boleto Tributo
        """
        length = len(number)

        if 47 <= length <= 48:
            data = {"code_line": number}
        elif length == 44:
            data = {"barcode": number}
        else:
            data = {}

        try:
            instance = BarcodeCobranca(**data)
            return instance
        except ValidationError:
            pass

        try:
            instance = BarcodeTributo(**data)
            return instance
        except ValidationError:
            pass

        raise ValueError("Código de barras ou linha digitável inválida!")

    def get_infos_from_barcode_or_code_line(self, number: str):
        """
        1. Identificar boleto
        2. Retornar informações
        """
        # 1
        instance = self.identify(number)

        # 2
        strategy_mapping = {
            BarcodeCobranca: BarcodeCobrancaService().get_infos_from_instance,  # noqa
            BarcodeTributo: BarcodeTributoService().get_infos_from_instance,  # noqa
        }
        action = strategy_mapping[instance.__class__]

        return action(instance)
