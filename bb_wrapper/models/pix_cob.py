from typing import Union, Optional

from pydantic import BaseModel, confloat, conint, constr, conlist

from .perfis import PessoaPix, EmpresaPix


class Calendario(BaseModel):
    expiracao: conint(gt=60)  # segundos até expiração


class Valor(BaseModel):
    original: confloat(ge=0.01)


class InfoAdicional(BaseModel):
    nome: constr(max_length=50)
    valor: constr(max_length=200)


class CobrancaPix(BaseModel):
    calendario: Calendario
    devedor: Union[PessoaPix, EmpresaPix]
    valor: Valor
    chave: constr(max_length=77)
    solicitacaoPagador: constr(max_length=140)
    infoAdicionais: Optional[conlist(InfoAdicional, max_items=50)]
