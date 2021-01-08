from enum import IntEnum
from typing import Optional, Literal

from pydantic import BaseModel, confloat, conint, constr

from .perfis import PessoaComEndereco, Pessoa


class ModalidadeEnum(IntEnum):
    """
    Código para identificar a característica dos boletos
    dentro das modalidades de cobrança existentes no BB.

    Inteiro, sendo 1 - SIMPLES ou 4 - VINCULADA
    """

    simples = 1
    vinculada = 4


class ConfiguracaoBaseTipoEnum(IntEnum):
    valor = 1
    porcentagem = 2


class ConfiguracaoBase(BaseModel):
    valor: Optional[confloat(strict=True, gt=0.0)]
    porcentagem: Optional[confloat(strict=True, gt=0.0)]


class BoletoConfiguracaoBase(ConfiguracaoBase):
    """
    Caso tipo seja 1: utilizar valor!

    Caso tipo seja 2: utilizar porcentagem!
    """

    tipo: ConfiguracaoBaseTipoEnum


class Multa(BoletoConfiguracaoBase):
    data: str


class DescontoBase(BaseModel):
    dataExpiracao: str


class PrimeiroDesconto(DescontoBase, BoletoConfiguracaoBase):
    pass


class SegundoOuTerceiroDesconto(DescontoBase, ConfiguracaoBase):
    pass


class Boleto(BaseModel):
    numeroConvenio: constr(max_length=7, min_length=7)
    numeroCarteira: str
    numeroVariacaoCarteira: str
    codigoModalidade: ModalidadeEnum
    dataEmissao: str
    dataVencimento: str
    valorOriginal: confloat(strict=True, gt=0.0)
    valorAbatimento: Optional[confloat(strict=True, gt=0.0)]
    quantidadeDiasProtesto: Optional[conint(ge=0)]
    indicadorNumeroDiasLimiteRecebimento: Optional[Literal["N", "S"]] = "N"
    numeroDiasLimiteRecebimento: Optional[conint(ge=0)]
    codigoAceite: Literal["A", "N"] = "N"
    codigoTipoTitulo: Literal[4] = 4
    descricaoTipoTitulo: Optional[str]
    indicadorPermissaoRecebimentoParcial: Literal["N", "S"] = "N"
    numeroTituloBeneficiario: Optional[str]
    textoCampoUtilizacaoBeneficiario: Optional[constr(max_length=30)]
    numeroTituloCliente: constr(max_length=20)
    textoMensagemBloquetoOcorrencia: Optional[constr(max_length=30)]
    pagador: PessoaComEndereco
    beneficiarioFinal: Optional[Pessoa]
    email: Optional[str]
    quantidadeDiasNegativacao: Optional[conint(ge=0)]

    jurosMora: Optional[BoletoConfiguracaoBase]
    multa: Optional[BoletoConfiguracaoBase]
    desconto: Optional[PrimeiroDesconto]
    segundoDesconto: Optional[SegundoOuTerceiroDesconto]
    terceiroDesconto: Optional[SegundoOuTerceiroDesconto]

    indicadorPix: Optional[Literal["S", "N"]]
