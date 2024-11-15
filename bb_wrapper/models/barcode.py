from pydantic.functional_validators import model_validator, field_validator
from typing_extensions import Annotated

from pydantic import BaseModel, StringConstraints

from ..services.barcode_cobranca import BarcodeCobrancaService
from ..services.barcode_tributo import BarcodeTributoService


class BarcodeCobranca(BaseModel):
    code_line: Annotated[
        str, StringConstraints(min_length=47, max_length=47, pattern=r"^\d+$")
    ] = None
    barcode: Annotated[
        str, StringConstraints(min_length=44, max_length=44, pattern=r"^\d+$")
    ] = None
    barcode_image: str = None

    @classmethod
    @field_validator("code_line")
    def _code_line_must_be_valid(cls, code_line):
        BarcodeCobrancaService().validate_code_line(code_line)
        return code_line

    @classmethod
    @field_validator("barcode")
    def _barcode_must_be_valid(cls, barcode):
        BarcodeCobrancaService().validate_barcode(barcode)
        return barcode

    @model_validator(mode="after")
    def _set_barcode_or_code_line(self):
        from ..services.barcode import BarcodeService

        code_line, barcode = self.code_line, self.barcode

        if code_line:
            self.barcode = BarcodeCobrancaService().code_line_to_barcode(code_line)
        elif barcode:
            self.code_line = BarcodeCobrancaService().barcode_to_code_line(barcode)
        else:
            raise ValueError("Informe a linha digitável ou código de barras!")

        self.barcode_image = BarcodeService().generate_barcode_b64image(self.barcode)
        return self


class BarcodeTributo(BaseModel):
    code_line: Annotated[
        str, StringConstraints(min_length=48, max_length=48, pattern=r"^\d+$")
    ] = None
    barcode: Annotated[
        str, StringConstraints(min_length=44, max_length=44, pattern=r"^\d+$")
    ] = None
    barcode_image: str = None

    @classmethod
    @field_validator("code_line")
    def _code_line_must_be_valid(cls, code_line):
        BarcodeTributoService().validate_code_line(code_line)
        return code_line

    @classmethod
    @field_validator("barcode")
    def _barcode_must_be_valid(cls, barcode):
        BarcodeTributoService().validate_barcode(barcode)
        return barcode

    @model_validator(mode="after")
    def _set_barcode_or_code_line(self):
        from ..services.barcode import BarcodeService

        code_line, barcode = self.code_line, self.barcode

        if code_line:
            self.barcode = BarcodeTributoService().code_line_to_barcode(code_line)
        elif barcode:
            self.code_line = BarcodeTributoService().barcode_to_code_line(barcode)
        else:
            raise ValueError("Informe a linha digitável ou código de barras!")

        self.barcode_image = BarcodeService().generate_barcode_b64image(self.barcode)
        return self
