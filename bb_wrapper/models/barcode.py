from typing import Optional

from pydantic import BaseModel, constr, validator, root_validator

from ..services.barcode_cobranca import BarcodeCobrancaService
from ..services.barcode_tributo import BarcodeTributoService


class BarcodeCobranca(BaseModel):
    code_line: Optional[constr(min_length=47, max_length=47, regex=r"^\d+$")]
    barcode: Optional[constr(min_length=44, max_length=44, regex=r"^\d+$")]
    barcode_image: Optional[str]

    # noinspection PyMethodParameters
    @validator("code_line")
    def _code_line_must_be_valid(cls, code_line):
        BarcodeCobrancaService().validate_code_line(code_line)
        return code_line

    # noinspection PyMethodParameters
    @validator("barcode")
    def _barcode_must_be_valid(cls, barcode):
        BarcodeCobrancaService().validate_barcode(barcode)
        return barcode

    # noinspection PyMethodParameters
    @root_validator
    def _set_data(cls, values):
        from ..services.barcode import BarcodeService

        code_line, barcode = values.get("code_line"), values.get("barcode")

        if code_line:
            values["barcode"] = BarcodeCobrancaService().code_line_to_barcode(code_line)
        elif barcode:
            values["code_line"] = BarcodeCobrancaService().barcode_to_code_line(barcode)
        else:
            raise ValueError("Informe a linha digitável ou código de barras!")

        values["barcode_image"] = BarcodeService().generate_barcode_b64image(
            values["barcode"]
        )
        return values


class BarcodeTributo(BaseModel):
    code_line: Optional[constr(min_length=48, max_length=48, regex=r"^\d+$")]
    barcode: Optional[constr(min_length=44, max_length=44, regex=r"^\d+$")]
    barcode_image: Optional[str]

    # noinspection PyMethodParameters
    @validator("code_line")
    def _code_line_must_be_valid(cls, code_line):
        BarcodeTributoService().validate_code_line(code_line)
        return code_line

    # noinspection PyMethodParameters
    @validator("barcode")
    def _barcode_must_be_valid(cls, barcode):
        BarcodeTributoService().validate_barcode(barcode)
        return barcode

    # noinspection PyMethodParameters
    @root_validator
    def _set_data(cls, values):
        from ..services.barcode import BarcodeService

        code_line, barcode = values.get("code_line"), values.get("barcode")

        if code_line:
            values["barcode"] = BarcodeTributoService().code_line_to_barcode(code_line)
        elif barcode:
            values["code_line"] = BarcodeTributoService().barcode_to_code_line(barcode)
        else:
            raise ValueError("Informe a linha digitável ou código de barras!")

        values["barcode_image"] = BarcodeService().generate_barcode_b64image(
            values["barcode"]
        )
        return values
