from enum import IntEnum

from pydantic import BaseModel, constr


class TipoInscricaoEnum(IntEnum):
    """
    1 - Pessoa Física
    2 - Pessoa Jurídica
    """

    cpf = 1
    cnpj = 2


class Pessoa(BaseModel):
    tipoInscricao: TipoInscricaoEnum
    numeroInscricao: int
    nome: constr(max_length=30)


class PessoaComEndereco(Pessoa):
    endereco: constr(max_length=30)
    cep: constr(max_length=8, min_length=8)
    cidade: constr(max_length=30)
    bairro: constr(max_length=30)
    uf: constr(max_length=2, min_length=2)
    telefone: constr(max_length=30) = None


class PessoaPix(BaseModel):
    cpf: constr(max_length=11, min_length=11)
    nome: str


class EmpresaPix(BaseModel):
    cnpj: constr(max_length=14, min_length=14)
    nome: str
