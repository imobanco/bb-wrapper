import io
from typing import Union

from barcode import generate as generate_barcode
from barcode.writer import SVGWriter

from pydantic import ValidationError

from .b64 import Base64Service
from ..models.barcode import BarcodeCobranca, BarcodeTributo


class BarcodeService:
    def generate_barcode_b64image(
        self, barcode: str, include_number_in_image=True
    ) -> str:
        """
        Método para gerar uma imagem base46 a partir de um código de barras numérico.
        """
        if include_number_in_image:
            text = barcode
        else:
            text = ""

        buffer = io.BytesIO()
        generate_barcode(
            name="itf",
            code=barcode,
            output=buffer,
            text=text,
            writer=SVGWriter(),
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
        return Base64Service().generate_b64image_from_buffer(buffer)

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
            raise ValueError("Tipo não identificado!")

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

        raise ValueError("Tipo não identificado!")
