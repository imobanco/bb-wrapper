from enum import IntEnum
from typing import Literal

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


class TipoBoletoEnum(IntEnum):
    APS = 20
    BA = 33
    BP = 32
    CH = 1
    CC = 31
    DAE = 24
    DAM = 25
    DAU = 23
    DM = 2
    DMI = 3
    DR = 6
    DS = 4
    DSI = 5
    FAT = 18
    LC = 7
    ME = 21
    NCC = 8
    NCE = 9
    NCI = 10
    NCR = 11
    ND = 19
    NP = 12
    NPR = 13
    NS = 16
    PCO = 22
    RCO = 17
    TM = 14
    TS = 15
    OUT = 99


class ConfiguracaoBaseTipoEnum(IntEnum):
    valor = 1
    porcentagem = 2


class ConfiguracaoBase(BaseModel):
    valor: confloat(strict=True, gt=0.0) = None
    porcentagem: confloat(strict=True, gt=0.0) = None


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
    indicadorAceiteTituloVencido: Literal["S", "N"] = "S"
    numeroDiasLimiteRecebimento: conint(ge=0) = None

    valorOriginal: confloat(strict=True, gt=0.0)
    valorAbatimento: confloat(strict=True, gt=0.0) = None
    indicadorPermissaoRecebimentoParcial: Literal["N", "S"] = "N"

    numeroTituloCliente: constr(max_length=20)
    pagador: PessoaComEndereco
    beneficiarioFinal: Pessoa = None

    quantidadeDiasProtesto: conint(ge=0) = None
    quantidadeDiasNegativacao: conint(ge=0) = None
    codigoAceite: Literal["A", "N"] = "N"
    codigoTipoTitulo: TipoBoletoEnum
    descricaoTipoTitulo: str = None
    numeroTituloBeneficiario: str = None
    textoCampoUtilizacaoBeneficiario: constr(max_length=30) = None
    textoMensagemBloquetoOcorrencia: constr(max_length=30) = None
    email: str = None

    jurosMora: BoletoConfiguracaoBase = None
    multa: BoletoConfiguracaoBase = None
    desconto: PrimeiroDesconto = None
    segundoDesconto: SegundoOuTerceiroDesconto = None
    terceiroDesconto: SegundoOuTerceiroDesconto = None

    indicadorPix: Literal["S", "N"] = None


class BoletoEstadoEnum(IntEnum):
    normal = 1
    movimento_cartorio = 2
    em_cartorio = 3
    titulo_com_ocorrencia_de_cartorio = 4
    protestado_eletronico = 5
    liquidado = 6
    baixado = 7
    titulo_com_pendencia_de_cartorio = 8
    titulo_protestado_manual = 9
    titulo_baixado_pago_em_cartorio = 10
    titulo_liquidado_protestado = 11
    titulo_liquidado_pgcrto = 12
    titulo_protestado_aguardando_baixa = 13
    titulo_em_liquidacao = 14
    titulo_agendado = 15
    titulo_creditado = 16
    pago_em_cheque_aguardando_liquidacao = 17
    pago_parcialmente = 18
    pago_parcialmente_credito = 19
