from typing import Optional, List, Union, Literal
from enum import IntEnum
from typing_extensions import Annotated

from pydantic import BaseModel, constr, Field, root_validator
from pycpfcnpj import cpfcnpj

from .perfis import TipoInscricaoEnum


class PagamentoTipoEnum(IntEnum):
    """
    126 - Pagamento a Fornecedores
    127 - Pagamento de Salários
    128 - Pagamentos Diversos
    """

    fornecedores = 126
    salarios = 127
    diversos = 128


class TipoChavePIX(IntEnum):
    """
    1 - Chave Pix tipo Telefone
    2 - Chave Pix tipo Email
    3 - Chave Pix tipo CPF/CNPJ
    4 - Chave Aleatória
    5 - Dados Bancários
    """

    telefone = 1
    email = 2
    documento = 3
    uuid = 4


class FinalidadeTED(IntEnum):
    """
    1 - Conta corrente outros bancos
    6 - Conta salário outros bancos
    11 - Poupança outros bancos
    """

    corrente = 1
    salario = 6
    poupanca = 11


class TransferenciaPIX(BaseModel):
    data: str
    valor: float
    chave: str
    formaIdentificacao: Optional[TipoChavePIX]
    dddTelefone: Optional[int]
    telefone: Optional[int]
    email: Optional[str]
    cpf: Optional[int]
    cnpj: Optional[int]
    identificacaoAleatoria: Optional[str]

    # noinspection PyMethodParameters
    @root_validator
    def _set_data(cls, values):
        from ..services.pix import PixService

        key = values.get("chave")

        key_type = PixService().identify_key_type(key)
        values["formaIdentificacao"] = key_type

        if key_type == TipoChavePIX.telefone:
            values["dddTelefone"] = int(key[:2])
            values["telefone"] = int(key[2:])
        elif key_type == TipoChavePIX.email:
            values["email"] = key
        elif key_type == TipoChavePIX.uuid:
            values["identificacaoAleatoria"] = key
        elif key_type == TipoChavePIX.documento:
            key_value = cpfcnpj.clear_punctuation(key)
            if len(key_value) == 1:
                values["cpf"] = int(key_value)
            else:
                values["cnpj"] = int(key_value)
        return values


class TransferenciaTED(BaseModel):
    numeroCOMPE: int
    agenciaCredito: int
    contaCorrenteCredito: int
    digitoVerificadorContaCorrente: str
    cpfBeneficiario: Optional[int]
    cnpjBeneficiario: Optional[int]
    dataTransferencia: str
    valorTransferencia: float
    codigoFinalidadeTED: Optional[FinalidadeTED]


class Boleto(BaseModel):
    numeroCodigoBarras: str
    dataPagamento: str
    valorPagamento: float
    descricaoPagamento: str
    valorNominal: float
    codigoTipoBeneficiario: TipoInscricaoEnum
    documentoBeneficiario: str


class Tributo(BaseModel):
    codigoBarras: str
    dataPagamento: str
    valorPagamento: float


class LoteData(BaseModel):
    n_requisicao: int
    agencia: int
    conta: int
    dv_conta: str
    convenio: Optional[int]


class LoteTransferenciaData(LoteData):
    tipo_pagamento: PagamentoTipoEnum
