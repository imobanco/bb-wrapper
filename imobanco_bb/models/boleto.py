from enum import IntEnum
from typing import Optional, Literal

from pydantic import BaseModel, confloat, PositiveInt, constr


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


class ModalidadeEnum(IntEnum):
    """
    Código para identificar a característica dos boletos dentro das modalidades de cobrança existentes no BB.
    Inteiro, sendo 1 - SIMPLES ou 4 - VINCULADA
    """
    simples = 1
    vinculada = 4


class Boleto(BaseModel):
    numeroConvenio: constr(max_length=7)
    numeroCarteira: str
    numeroVariacaoCarteira: str
    codigoModalidade: ModalidadeEnum
    dataEmissao: str
    dataVencimento: str
    valorOriginal: confloat(strict=True, gt=0.0)
    valorAbatimento: Optional[confloat(strict=True, gt=0.0)]
    quantidadeDiasProtesto: Optional[PositiveInt]
    indicadorNumeroDiasLimiteRecebimento: Optional[Literal['N', 'S']] = 'N'
    numeroDiasLimiteRecebimento: Optional[PositiveInt]
    codigoAceite: Literal['A', 'N'] = 'N'
    codigoTipoTitulo: Literal[4] = 4
    descricaoTipoTitulo: Optional[str]
    indicadorPermissaoRecebimentoParcial: Literal['N', 'S'] = 'N'
    numeroTituloBeneficiario: Optional[str]
    textoCampoUtilizacaoBeneficiario: Optional[constr(max_length=30)]
    numeroTituloCliente: constr(max_length=20)
    textoMensagemBloquetoOcorrencia: Optional[constr(max_length=30)]
    pagador: Pagador
    email: Optional[str]
