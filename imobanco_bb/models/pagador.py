from enum import IntEnum

from pydantic import BaseModel


class TipoRegistroEnum(IntEnum):
    """
    1 - Pessoa Física
    2 - Pessoa Jurídica
    """

    cpf = 1
    cnpj = 2


class Pagador(BaseModel):
    tipoRegistro: TipoRegistroEnum
    numeroRegistro: str
    nome: str
    endereco: str
    cep: str
    cidade: str
    bairro: str
    uf: str
    telefone: str
