from typing import Optional
from enum import IntEnum

from pydantic import BaseModel, constr


class TipoRegistroEnum(IntEnum):
    """
    1 - Pessoa Física
    2 - Pessoa Jurídica
    """

    cpf = 1
    cnpj = 2


class Pagador(BaseModel):
    tipoRegistro: TipoRegistroEnum
    numeroRegistro: constr(max_length=14, min_length=11)
    nome: constr(max_length=30)
    endereco: constr(max_length=30)
    cep: constr(max_length=8, min_length=8)
    cidade: constr(max_length=30)
    bairro: constr(max_length=30)
    uf: constr(max_length=2, min_length=2)
    telefone: Optional[constr(max_length=30)]


class Avalista(BaseModel):
    tipoRegistro: TipoRegistroEnum
    numeroRegistro: constr(max_length=14, min_length=11)
    nomeRegistro: constr(max_length=30)
