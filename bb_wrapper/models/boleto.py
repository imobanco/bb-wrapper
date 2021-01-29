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
    indicadorAceiteTituloVencido: Optional[Literal["S", "N"]] = "S"
    numeroDiasLimiteRecebimento: Optional[conint(ge=0)]

    valorOriginal: confloat(strict=True, gt=0.0)
    valorAbatimento: Optional[confloat(strict=True, gt=0.0)]
    indicadorPermissaoRecebimentoParcial: Literal["N", "S"] = "N"

    numeroTituloCliente: constr(max_length=20)
    pagador: PessoaComEndereco
    beneficiarioFinal: Optional[Pessoa]

    quantidadeDiasProtesto: Optional[conint(ge=0)]
    quantidadeDiasNegativacao: Optional[conint(ge=0)]
    codigoAceite: Literal["A", "N"] = "N"
    codigoTipoTitulo: Literal[4] = 4
    descricaoTipoTitulo: Optional[str]
    numeroTituloBeneficiario: Optional[str]
    textoCampoUtilizacaoBeneficiario: Optional[constr(max_length=30)]
    textoMensagemBloquetoOcorrencia: Optional[constr(max_length=30)]
    email: Optional[str]

    jurosMora: Optional[BoletoConfiguracaoBase]
    multa: Optional[BoletoConfiguracaoBase]
    desconto: Optional[PrimeiroDesconto]
    segundoDesconto: Optional[SegundoOuTerceiroDesconto]
    terceiroDesconto: Optional[SegundoOuTerceiroDesconto]

    indicadorPix: Optional[Literal["S", "N"]]


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
