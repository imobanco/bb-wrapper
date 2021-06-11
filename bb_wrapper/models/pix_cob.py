from typing import Union

from pydantic import BaseModel, confloat, conint

from .perfis import PessoaPix, EmpresaPix


class Calendario(BaseModel):
    expiracao: conint(gt=60)  # segundos até expiração


class Valor(BaseModel):
    original: confloat(gt=0.01)


class CobrancaPix(BaseModel):
    calendario: Calendario
    devedor: Union[PessoaPix, EmpresaPix]
    valor: Valor
    chave: str
    solicitacaoPagador: str
