from typing import Optional
from enum import IntEnum, Enum

from pydantic import BaseModel, root_validator
from pycpfcnpj import cpfcnpj

from .perfis import TipoInscricaoEnum


class IndicadorFloatEnum(Enum):
    s = "S"
    n = "N"


class PagamentoTipoEnum(IntEnum):
    """
    126: Pagamento a Fornecedores
    127: Pagamento de Salários
    128: Pagamentos Diversos
    """

    fornecedores = 126
    salarios = 127
    diversos = 128


class TipoChavePIX(IntEnum):
    """
    1: Chave Pix tipo Telefone
    2: Chave Pix tipo Email
    3: Chave Pix tipo CPF/CNPJ
    4: Chave Aleatória
    5: Dados Bancários
    """

    telefone = 1
    email = 2
    documento = 3
    uuid = 4


class FinalidadeTED(IntEnum):
    """
    1: Conta corrente outros bancos
    6: Conta salário outros bancos
    11: Poupança outros bancos
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
        """
        Esse método realiza o processamento em cima do valor 'chave'
        identificando que tipo de chave é e configurando-a corretamente
        no objeto.
        """
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


class LiberarPagamentos(BaseModel):
    numeroRequisicao: int
    indicadorFloat: IndicadorFloatEnum


STATUS_PAGAMENTO_DICT = {
    "VENCIDO": "Pagamento não efetuado na data indicada por falta de saldo ou falta de autorização para débito do pagamento na conta do cliente conveniado.",  # noqa: E501
    "CONSISTENTE": "pagamento recebido pelo banco, cumprem as regras de preenchimento dos campos mas ainda irá para validação e processamento",  # noqa: E501
    "INCONSISTENTE": "pagamento não aceito pelo banco por dados de entrada inconsistentes. Não cumpre as regras de preenchimento dos campos",  # noqa: E501
    "PAGO": "pagamento efetuado ao favorecido",
    "PENDENTE": "pagamento validado. Pendência de autorização do pagamento por parte do pagador",  # noqa: E501
    "AGUARDANDO SALDO": "débito não efetivado e em verificação de saldo até o horário limite da teimosinha.",  # noqa: E501
    "AGENDADO": "pagamento autorizado, porém aguardando a data de efetivação do pagamento ou horário de processamento",  # noqa: E501
    "REJEITADO": "dados do pagamento não passaram na validações físicas e/ou lógicas, precisam ser corrigidos e reenviados. Ex: agência e conta não existem, conta não pertence ao CPF informado",  # noqa: E501
    "CANCELADO": "pagamento cancelado pelo pagador antes da data de efetivação do crédito",  # noqa: E501
    "BLOQUEADO": "Débito na conta do pagador não efetivado por ocorrência no convênio, inconsistência de data/float ou falta de saldo",  # noqa: E501
    "DEVOLVIDO": "pagamento efetuado e posteriormente devolvido pelo favorecido ou instituição recebedora. O valor é devolvido para a conta corrente onde ocorreu o débito da requisição",  # noqa: E501
    "DEBITADO": "pagamento debitado na conta do pagador e pendente de crédito ao favorecido",  # noqa: E501
}

STATUS_LOTE_DICT = {
    1: "Requisição com todos os lançamentos com dados consistentes",
    2: "Requisição com ao menos um dos lançamentos com dados inconsistentes",
    3: "Requisição com todos os lançamentos com dados inconsistentes",
    4: "Requisição pendente de ação pelo Conveniado. Falta autorizar o pagamento",
    5: "Requisição em processamento pelo Banco",
    6: "Requisição Processada",
    7: "Requisição Rejeitada",
    8: "Preparando remessa não liberada",
    9: "Requisição liberada via API",
    10: "Preparando remessa liberada",
}

ERROS_VALIDACAO_PAGAMENTO_DICT = {
    1: {
        "codigo": 1,
        "texto_tecnico": "Agência de crédito igual a zero. Informe o número da Agência de Crédito.",  # noqa
    },
    2: {
        "codigo": 2,
        "texto_tecnico": "Conta de crédito não é numérica. Informe apenas números.",
    },
    3: {
        "codigo": 3,
        "texto_tecnico": "Dígito da conta de crédito igual a espaços. Informe o DV da conta de crédito.",  # noqa
    },
    4: {
        "codigo": 4,
        "texto_tecnico": "CPF não é numérico. Informe apenas números.",
    },
    5: {
        "codigo": 5,
        "texto_tecnico": "CNPJ não é numérico. Informe apenas números.",
    },
    6: {
        "codigo": 6,
        "texto_tecnico": "Data do pagamento igual a zeros. Informe a data do pagamento.",  # noqa
    },
    7: {
        "codigo": 7,
        "texto_tecnico": "Data do pagamento inválida. Informe uma data de pagamento válida.",  # noqa
    },
    8: {
        "codigo": 8,
        "texto_tecnico": "Valor do pagamento não é númerico. Informe apenas números.",  # noqa
    },
    9: {
        "codigo": 9,
        "texto_tecnico": "Valor do pagamento igual a zeros. Informe o valor do pagamento.",  # noqa
    },
    10: {
        "codigo": 10,
        "texto_tecnico": "Ambos os campos Número Compensação e Número ISPB estão zerados. Informe um dos campos.",  # noqa
    },
    11: {
        "codigo": 11,
        "texto_tecnico": "Ambos os campos Número Compensação e Número ISPB foram informados. Informe apenas um dos campos.",  # noqa
    },
    12: {
        "codigo": 12,
        "texto_tecnico": "Ambos os campos Finalidade DOC e Finalidade TED estão zerados. Informe um dos campos.",  # noqa
    },
    13: {
        "codigo": 13,
        "texto_tecnico": "Ambos os campos Finalidade DOC e Finalidade TED foram informados. Informe apenas um dos campos.",  # noqa
    },
    14: {
        "codigo": 14,
        "texto_tecnico": "Número depósito judicial igual a espaços.",
    },
    15: {
        "codigo": 15,
        "texto_tecnico": "Dígito da conta de crédito inválido.",
    },
    16: {
        "codigo": 16,
        "texto_tecnico": "Ambos os campos CPF e CNPJ foram informados. Informe apenas um dos campos. Caso informado os 2 campos, nas consultas será exibido apenas os dados do CPF.",  # noqa
    },
    17: {
        "codigo": 17,
        "texto_tecnico": "Ambos os campos CPF e CNPJ estão zerados. Informe um dos campos.",  # noqa
    },
    18: {
        "codigo": 18,
        "texto_tecnico": "Dígito do CPF inválido. Verifique o dado informado.",
    },
    19: {
        "codigo": 19,
        "texto_tecnico": "Dígito do CNPJ inválido. Verifique o dado informado.",  # noqa
    },
    20: {
        "codigo": 20,
        "texto_tecnico": "Agência e conta de crédito estão iguais a de débito. Opção não permitida.",  # noqa
    },
    21: {
        "codigo": 21,
        "texto_tecnico": "Número Compensação inválido. Verifique o dado informado.",  # noqa
    },
    22: {
        "codigo": 22,
        "texto_tecnico": "Número ISPB diferente de zeros. Não informe o número ISPB.",  # noqa
    },
    23: {
        "codigo": 23,
        "texto_tecnico": "Conta de crédito igual a zeros. Informe o número da conta de crédito.",  # noqa
    },
    24: {
        "codigo": 24,
        "texto_tecnico": "CPF igual a zeros. Obrigatório informar o número do CPF.",  # noqa
    },
    25: {
        "codigo": 25,
        "texto_tecnico": "CNPJ diferente de zeros. Não permitido informar CNPJ.",  # noqa
    },
    26: {
        "codigo": 26,
        "texto_tecnico": "Conta de crédito diferente de zeros. Não permitido informar Conta de crédito.",  # noqa,
    },
    27: {
        "codigo": 27,
        "texto_tecnico": "Dígito conta de crédito diferente de espaços. Não informar dígito da conta de crédito.",  # noqa
    },
    28: {
        "codigo": 28,
        "texto_tecnico": "Finalidade DOC diferente de zeros. Não informar finalidade DOC.",  # noqa
    },
    29: {
        "codigo": 29,
        "texto_tecnico": "Finalidade TED diferente de zeros. Não informar finalidade TED.",  # noqa
    },
    30: {
        "codigo": 30,
        "texto_tecnico": "Número Depósito Judicial diferente de espaços. Não informar finalidade Depósito Judicial.",  # noqa
    },
    31: {
        "codigo": 31,
        "texto_tecnico": "Número do documento de crédito não é numérico. Informar números.",  # noqa
    },
    32: {
        "codigo": 32,
        "texto_tecnico": "Número do documento de débito não é numérico. Informar números.",  # noqa
    },
    33: {
        "codigo": 33,
        "texto_tecnico": "CPF não encontrado na base da receita federal.",
    },
    34: {
        "codigo": 34,
        "texto_tecnico": "CNPJ não encontrado na base da receita federal.",
    },
    35: {
        "codigo": 35,
        "texto_tecnico": "Conta de poupança não permitido. Para creditar poupança utilize Código Produto igual a 128 - Pagamentos Diversos.",  # noqa
    },
    36: {
        "codigo": 36,
        "texto_tecnico": "Código COMPE deve ser igual a 1.",
    },
    37: {
        "codigo": 37,
        "texto_tecnico": "Código ISPB deve ser igual a 0.",
    },
    38: {
        "codigo": 38,
        "texto_tecnico": "Código de barras não é numérico. Informar números.",
    },
    39: {
        "codigo": 39,
        "texto_tecnico": "Código de barras igual a zeros. Informar números.",
    },
    40: {
        "codigo": 40,
        "texto_tecnico": "Número de inscrição do pagador não é numérico. Informar números.",  # noqa
    },
    41: {
        "codigo": 41,
        "texto_tecnico": "Número de inscrição do beneficiário não é numérico. Informar números.",  # noqa
    },
    42: {
        "codigo": 42,
        "texto_tecnico": "Número de inscrição do avalista não é numérico. Informar números.",  # noqa
    },
    43: {
        "codigo": 43,
        "texto_tecnico": "Dígito do CPF para o pagador inválido. Verifique o número correto.",  # noqa
    },
    44: {
        "codigo": 44,
        "texto_tecnico": "Dígito do CPF para o beneficiário inválido. Verifique o número correto.",  # noqa
    },
    45: {
        "codigo": 45,
        "texto_tecnico": "Dígito do CPF para o avalista inválido. Verifique o número correto.",  # noqa
    },
    46: {
        "codigo": 46,
        "texto_tecnico": "Dígito do CNPJ para o pagador inválido. Verifique o número correto.",  # noqa
    },
    47: {
        "codigo": 47,
        "texto_tecnico": "Dígito do CNPJ para o beneficiário inválido. Verifique o número correto.",  # noqa
    },
    48: {
        "codigo": 48,
        "texto_tecnico": "Dígito do CNPJ para o avalista inválido. Verifique o número correto.",  # noqa
    },
    49: {
        "codigo": 49,
        "texto_tecnico": "Data do vencimento inválida.  Informar data válida.",
    },
    50: {
        "codigo": 50,
        "texto_tecnico": "Valor nominal não é numérico. Informar números.",
    },
    51: {
        "codigo": 51,
        "texto_tecnico": "Valor de desconto não é numérico. Informar números.",
    },
    52: {
        "codigo": 52,
        "texto_tecnico": "Valor de mora não é numérico. Informar números.",
    },
    53: {
        "codigo": 53,
        "texto_tecnico": "Data do pagamento deve ser maior ou igual ao dia atual.",  # noqa
    },
    54: {
        "codigo": 54,
        "texto_tecnico": "Número do documento de débito igual a zeros.",
    },
    55: {
        "codigo": 55,
        "texto_tecnico": "Data do vencimento igual a zeros. Informar data de vencimento.",  # noqa
    },
    56: {
        "codigo": 56,
        "texto_tecnico": "Nome do beneficiário não informado.",
    },
    57: {
        "codigo": 57,
        "texto_tecnico": "Número de inscrição do beneficiário não informado. Obrigatório informar o CPF ou CNPJ do beneficiário.",  # noqa
    },
    58: {
        "codigo": 58,
        "texto_tecnico": "Conta pagamento diferente de espaços. Não informar conta pagamento.",  # noqa
    },
    59: {
        "codigo": 59,
        "texto_tecnico": "Ambos os campos conta de crédito e conta pagamento foram informados. Informar apenas um dos campos.",  # noqa
    },
    60: {
        "codigo": 60,
        "texto_tecnico": "Transação cancelada pelo cliente.",
    },
    61: {
        "codigo": 61,
        "texto_tecnico": "Código da Receita do Tributo não informado.",
    },
    62: {
        "codigo": 62,
        "texto_tecnico": "Tipo de Identificação do Contribuinte não informado.",  # noqa
    },
    63: {
        "codigo": 63,
        "texto_tecnico": "Número de Identificação do Contribuinte não informado.",
    },
    64: {
        "codigo": 64,
        "texto_tecnico": "Número de Identificação do Contribuinte não numérico.",
    },
    65: {
        "codigo": 65,
        "texto_tecnico": "Código de Identificação do Tributo não informado.",
    },
    66: {
        "codigo": 66,
        "texto_tecnico": "Período de apuração não informado.",
    },
    67: {
        "codigo": 67,
        "texto_tecnico": "Número de Referência não informado.",
    },
    68: {
        "codigo": 68,
        "texto_tecnico": "Valor Principal não é numérico.",
    },
    69: {
        "codigo": 69,
        "texto_tecnico": "Valor Principal não informado.",
    },
    70: {
        "codigo": 70,
        "texto_tecnico": "Valor da Multa não é numérico.",
    },
    71: {
        "codigo": 71,
        "texto_tecnico": "Valor dos Juros/Encargos não é numérico.",
    },
    72: {
        "codigo": 72,
        "texto_tecnico": "Data de Vencimento não informada.",
    },
    73: {
        "codigo": 73,
        "texto_tecnico": "Mês e ano de competência não informados.",
    },
    74: {
        "codigo": 74,
        "texto_tecnico": "Valor previsto do pagamento do INSS não é numérico.",
    },
    75: {
        "codigo": 75,
        "texto_tecnico": "Valor previsto do pagamento do INSS não informado.",
    },
    76: {
        "codigo": 76,
        "texto_tecnico": "Valor de Outras Entidades não é numérico.",
    },
    77: {
        "codigo": 77,
        "texto_tecnico": "Valor de Atualização Monetária não é numérico.",
    },
    78: {
        "codigo": 78,
        "texto_tecnico": "Valor de Atualização Monetária não é numérico.",
    },
    79: {
        "codigo": 79,
        "texto_tecnico": "Período de apuração inválido.",
    },
    80: {
        "codigo": 80,
        "texto_tecnico": "Conta de crédito inválida. Informe o número sem o 45 do início.",  # noqa
    },
    81: {
        "codigo": 81,
        "texto_tecnico": "A conta informada não pertence ao funcionário.",
    },
    82: {
        "codigo": 82,
        "texto_tecnico": "Pagamento permitido apenas para pessoas físicas.",
    },
    83: {
        "codigo": 83,
        "texto_tecnico": "Agência e Conta incorretas.",
    },
    84: {
        "codigo": 84,
        "texto_tecnico": "A conta informada não está ativa.",
    },
    85: {
        "codigo": 85,
        "texto_tecnico": "Conta não permite crédito de salário. Informe outra conta.",  # noqa
    },
    86: {
        "codigo": 86,
        "texto_tecnico": "Ambos os campos agência de crédito e conta pagamento foram informados.",  # noqa
    },
    90: {
        "codigo": 90,
        "texto_tecnico": "Mês de competência inválido.",
    },
    91: {
        "codigo": 91,
        "texto_tecnico": "Valor de outras deduções inválido.",
    },
    92: {
        "codigo": 92,
        "texto_tecnico": "Valor de outros acréscimos inválido.",
    },
    93: {
        "codigo": 93,
        "texto_tecnico": "Código da forma de identificação do cliente não foi informado.",  # noqa
    },
    94: {
        "codigo": 94,
        "texto_tecnico": "DDD do cliente do PIX não foi informado.",
    },
    95: {
        "codigo": 95,
        "texto_tecnico": "Telefone do Cliente do PIX não foi informado.",
    },
    96: {
        "codigo": 96,
        "texto_tecnico": "Email do cliente do PIX não foi informado.",
    },
    97: {
        "codigo": 97,
        "texto_tecnico": "Chave Aleatória do Cliente do PIX não foi informada.",  # noqa
    },
    98: {
        "codigo": 98,
        "texto_tecnico": "Código de tipo de conta do Cliente do PIX não foi informado.",  # noqa
    },
    99: {
        "codigo": 99,
        "texto_tecnico": "Consultar o Banco para detalhar o erro.",
    },
    100: {
        "codigo": 100,
        "texto_tecnico": "E-mail inválido.",
    },
    101: {
        "codigo": 101,
        "texto_tecnico": "Email do cliente do PIX não deve conter caractere especial.",  # noqa
    },
    102: {
        "codigo": 102,
        "texto_tecnico": "Telefone Inválido.",
    },
    103: {
        "codigo": 103,
        "texto_tecnico": "DDD inválido.",
    },
    104: {
        "codigo": 104,
        "texto_tecnico": "E-mail com tamanho maior que 77 caracteres.",
    },
    105: {
        "codigo": 105,
        "texto_tecnico": "Conta de crédito inválida. Informe um número de conta válido.",  # noqa
    },
    106: {
        "codigo": 106,
        "texto_tecnico": "CPF inválido. Informe um CPF válido.",
    },
    107: {
        "codigo": 107,
        "texto_tecnico": "CNPJ inválido. Informe um CNPJ válido.",
    },
    108: {
        "codigo": 108,
        "texto_tecnico": "Número do documento de crédito inválido. Informe um número válido.",  # noqa
    },
    109: {
        "codigo": 109,
        "texto_tecnico": "Número do documento de débito inválido. Informe um número válido.",  # noqa
    },
    110: {
        "codigo": 110,
        "texto_tecnico": "Valor do pagamento inválido. Informe um valor válido.",  # noqa
    },
    111: {
        "codigo": 111,
        "texto_tecnico": "Valor nominal inválido. Informe um valor válido.",
    },
    112: {
        "codigo": 112,
        "texto_tecnico": "Valor de desconto inválido. Informe um valor válido.",  # noqa
    },
    113: {
        "codigo": 113,
        "texto_tecnico": "Valor de mora inválido. Informe um valor válido.",
    },
    114: {
        "codigo": 114,
        "texto_tecnico": "Número de inscrição do beneficiário inválido. Informe um número válido.",  # noqa
    },
    115: {
        "codigo": 115,
        "texto_tecnico": "Número de inscrição do pagador inválido. Informe um número válido.",  # noqa
    },
    116: {
        "codigo": 116,
        "texto_tecnico": "Número de inscrição do avalista inválido. Informe um número válido.",  # noqa
    },
    117: {
        "codigo": 117,
        "texto_tecnico": "Número de identifiação do contribuinte DARF (Documento de Arrecadação de Receitas Federais) inválido. Informe um número válido.",  # noqa
    },
    118: {
        "codigo": 118,
        "texto_tecnico": "Número de referência inválido. Informe um número válido.",  # noqa
    },
    119: {
        "codigo": 119,
        "texto_tecnico": "Valor principal inválido. Informe um valor válido.",
    },
    120: {
        "codigo": 120,
        "texto_tecnico": "Valor da multa inválido. Informe um valor válido.",
    },
    121: {
        "codigo": 121,
        "texto_tecnico": "Valor dos juros/encargos inválido. Informe um valor válido.",  # noqa
    },
    122: {
        "codigo": 122,
        "texto_tecnico": "Número de identificação do contribuinte GPS (Guia da Previdência Social) inválido. Informe um número válido.",  # noqa
    },
    123: {
        "codigo": 123,
        "texto_tecnico": "Valor previsto do pagamento do INSS inválido. Informe um valor válido.",  # noqa
    },
    124: {
        "codigo": 124,
        "texto_tecnico": "Valor de outras entidades inválido. Informe um valor válido.",  # noqa
    },
    125: {
        "codigo": 125,
        "texto_tecnico": "Valor de atualização monetária inválido. Informe um valor válido.",  # noqa
    },
    126: {
        "codigo": 126,
        "texto_tecnico": "Valor de desconto GRU inválido. Informe um valor válido.",  # noqa
    },
    200: {
        "codigo": 200,
        "texto_tecnico": "Insuficiência de Fundos - Débito Não Efetuado.",
    },
    201: {
        "codigo": 201,
        "texto_tecnico": "Crédito ou Débito Cancelado pelo Pagador.",
    },
    202: {
        "codigo": 202,
        "texto_tecnico": "Débito Autorizado pela Agência - Efetuado.",
    },
    203: {
        "codigo": 203,
        "texto_tecnico": "Controle Inválido. Verificar campos 01, 02 e 03 do header ou segmento A, B, C, J, J52, N, O ou W do Arquivo CNAB240.",  # noqa
    },
    204: {
        "codigo": 204,
        "texto_tecnico": "Tipo de Operação Inválido.",
    },
    205: {
        "codigo": 205,
        "texto_tecnico": "Tipo de Serviço Inválido. Utilize 126 para Pagamento a Fornecedores, 127 para Pagamento de Salários ou 128 para Pagamentos Diversos.",  # noqa
    },
    206: {
        "codigo": 206,
        "texto_tecnico": "Forma de Lançamento Inválida. Para crédito em Poupança utilize Pagamentos Diversos. Para crédito em Conta Pagamento utilize Pagamentos Diversos ou Pagamento a Fornecedores. Para Pagamento de salário a conta de crédito deve ser do BB.",  # noqa
    },
    207: {
        "codigo": 207,
        "texto_tecnico": "Tipo/Número de Inscrição Inválido. CPF ou CNPJ inválido.",  # noqa
    },
    208: {
        "codigo": 208,
        "texto_tecnico": "Código de Convênio Inválido.",
    },
    209: {
        "codigo": 209,
        "texto_tecnico": "Agência/Conta Corrente/DV Inválido.",
    },
    210: {
        "codigo": 210,
        "texto_tecnico": "Número Sequencial do Registro no Lote Inválido.",
    },
    211: {
        "codigo": 211,
        "texto_tecnico": "Código de Segmento de Detalhe Inválido.",
    },
    212: {
        "codigo": 212,
        "texto_tecnico": "Lançamento inconsistente, rejeitado na prévia. Corrigir os dados do lançamento e enviar novo pagamento.",  # noqa
    },
    213: {
        "codigo": 213,
        "texto_tecnico": "Número COMPE do Banco para crédito Inválido.",
    },
    214: {
        "codigo": 214,
        "texto_tecnico": "Número do ISPB (Identificador de Sistema de Pagamentos Brasileiro) Banco, Instituição de Pagamento para crédito Inválido.",  # noqa
    },
    215: {
        "codigo": 215,
        "texto_tecnico": "Agência Mantenedora da Conta Corrente do Favorecido Inválida.",  # noqa
    },
    216: {
        "codigo": 216,
        "texto_tecnico": "Conta Corrente/DV/Conta de Pagamento do Favorecido Inválido.",  # noqa
    },
    217: {
        "codigo": 217,
        "texto_tecnico": "Nome do Favorecido Não Informado.",
    },
    218: {
        "codigo": 218,
        "texto_tecnico": "Data de Lançamento Inválida.",
    },
    219: {
        "codigo": 219,
        "texto_tecnico": "Tipo/Quantidade da Moeda Inválido.",
    },
    220: {
        "codigo": 220,
        "texto_tecnico": "Valor do Lançamento Inválido.",
    },
    221: {
        "codigo": 221,
        "texto_tecnico": "Aviso ao Favorecido - Identificação Inválida.",
    },
    222: {
        "codigo": 222,
        "texto_tecnico": "Tipo/Número de Inscrição do Favorecido Inválido. CPF ou CNPJ do favorecido inválido.",  # noqa
    },
    223: {
        "codigo": 223,
        "texto_tecnico": "Logradouro do Favorecido Não Informado.",
    },
    224: {
        "codigo": 224,
        "texto_tecnico": "Número do Local do Favorecido Não Informado.",
    },
    225: {
        "codigo": 225,
        "texto_tecnico": "Cidade do Favorecido Não Informada.",
    },
    226: {
        "codigo": 226,
        "texto_tecnico": "CEP/Complemento do Favorecido Inválido.",
    },
    227: {
        "codigo": 227,
        "texto_tecnico": "Sigla do Estado do Favorecido Inválida.",
    },
    228: {
        "codigo": 228,
        "texto_tecnico": "Número do Banco para crédito Inválido.",
    },
    229: {
        "codigo": 229,
        "texto_tecnico": "Código/Nome da Agência Depositária Não Informado.",
    },
    230: {
        "codigo": 230,
        "texto_tecnico": "Seu Número Inválido.",
    },
    231: {
        "codigo": 231,
        "texto_tecnico": "Nosso Número Inválido.",
    },
    232: {
        "codigo": 232,
        "texto_tecnico": "Inclusão Efetuada com Sucesso.",
    },
    233: {
        "codigo": 233,
        "texto_tecnico": "Alteração Efetuada com Sucesso.",
    },
    234: {
        "codigo": 234,
        "texto_tecnico": "Exclusão Efetuada com Sucesso.",
    },
    235: {
        "codigo": 235,
        "texto_tecnico": "Agência/Conta Impedida Legalmente.",
    },
    236: {
        "codigo": 236,
        "texto_tecnico": "Empresa não pagou salário. Conta de crédito só aceita pagamento de salário.",  # noqa
    },
    237: {
        "codigo": 237,
        "texto_tecnico": "Falecimento do mutuário.",
    },
    238: {
        "codigo": 238,
        "texto_tecnico": "Empresa não enviou remessa do mutuário.",
    },
    239: {
        "codigo": 239,
        "texto_tecnico": "Empresa não enviou remessa no vencimento.",
    },
    240: {
        "codigo": 240,
        "texto_tecnico": "Valor da parcela inválida.",
    },
    241: {
        "codigo": 241,
        "texto_tecnico": "Identificação do contrato inválida.",
    },
    242: {
        "codigo": 242,
        "texto_tecnico": "Operação de Consignação Incluída com Sucesso.",
    },
    243: {
        "codigo": 243,
        "texto_tecnico": "Operação de Consignação Alterada com Sucesso.",
    },
    244: {
        "codigo": 244,
        "texto_tecnico": "Operação de Consignação Excluída com Sucesso.",
    },
    245: {
        "codigo": 245,
        "texto_tecnico": "Operação de Consignação Liquidada com Sucesso.",
    },
    246: {
        "codigo": 246,
        "texto_tecnico": "Reativação Efetuada com Sucesso.",
    },
    247: {
        "codigo": 247,
        "texto_tecnico": "Suspensão Efetuada com Sucesso.",
    },
    248: {
        "codigo": 248,
        "texto_tecnico": "Código de Barras - Código do Banco Inválido.",
    },
    249: {
        "codigo": 249,
        "texto_tecnico": "Código de Barras - Código da Moeda Inválido.",
    },
    250: {
        "codigo": 250,
        "texto_tecnico": "Código de Barras - Dígito Verificador Geral Inválido.",  # noqa
    },
    251: {
        "codigo": 251,
        "texto_tecnico": "Código de Barras - Valor do Título Inválido.",
    },
    252: {
        "codigo": 252,
        "texto_tecnico": "Código de Barras - Campo Livre Inválido.",
    },
    253: {
        "codigo": 253,
        "texto_tecnico": "Valor do Documento Inválido.",
    },
    254: {
        "codigo": 254,
        "texto_tecnico": "Valor do Abatimento Inválido.",
    },
    255: {
        "codigo": 255,
        "texto_tecnico": "Valor do Desconto Inválido.",
    },
    256: {
        "codigo": 256,
        "texto_tecnico": "Valor de Mora Inválido.",
    },
    257: {
        "codigo": 257,
        "texto_tecnico": "Valor da Multa Inválido.",
    },
    258: {
        "codigo": 258,
        "texto_tecnico": "Valor do IR Inválido.",
    },
    259: {
        "codigo": 259,
        "texto_tecnico": "Valor do ISS Inválido.",
    },
    260: {
        "codigo": 260,
        "texto_tecnico": "Valor do IOF Inválido.",
    },
    261: {
        "codigo": 261,
        "texto_tecnico": "Valor de Outras Deduções Inválido.",
    },
    262: {
        "codigo": 262,
        "texto_tecnico": "Valor de Outros Acréscimos Inválido.",
    },
    263: {
        "codigo": 263,
        "texto_tecnico": "Valor do INSS Inválido.",
    },
    264: {
        "codigo": 264,
        "texto_tecnico": "Lote Não Aceito.",
    },
    265: {
        "codigo": 265,
        "texto_tecnico": "Inscrição da Empresa Inválida para o Contrato.",
    },
    266: {
        "codigo": 266,
        "texto_tecnico": "Convênio com a Empresa Inexistente/Inválido para o Contrato.",
    },
    267: {
        "codigo": 267,
        "texto_tecnico": "Agência/Conta Corrente da Empresa Inexistente/Inválida para o Contrato.",  # noqa
    },
    268: {
        "codigo": 268,
        "texto_tecnico": "Tipo de Serviço Inválido para o Contrato.",
    },
    269: {
        "codigo": 269,
        "texto_tecnico": "Conta Corrente da Empresa com Saldo Insuficiente.",
    },
    270: {
        "codigo": 270,
        "texto_tecnico": "Lote de Serviço Fora de Sequência.",
    },
    271: {
        "codigo": 271,
        "texto_tecnico": "Lote de Serviço Inválido.",
    },
    272: {
        "codigo": 272,
        "texto_tecnico": "Arquivo não aceito.",
    },
    273: {
        "codigo": 273,
        "texto_tecnico": "Tipo de Registro Inválido.",
    },
    274: {
        "codigo": 274,
        "texto_tecnico": "Código Remessa/Retorno Inválido.",
    },
    275: {
        "codigo": 275,
        "texto_tecnico": "Versão de layout inválida.",
    },
    276: {
        "codigo": 276,
        "texto_tecnico": "Mutuário não identificado.",
    },
    277: {
        "codigo": 277,
        "texto_tecnico": "Tipo do beneficio não permite empréstimo.",
    },
    278: {
        "codigo": 278,
        "texto_tecnico": "Beneficio cessado/suspenso.",
    },
    279: {
        "codigo": 279,
        "texto_tecnico": "Beneficio possui representante legal.",
    },
    280: {
        "codigo": 280,
        "texto_tecnico": "Beneficio é do tipo PA (Pensão alimentícia).",
    },
    281: {
        "codigo": 281,
        "texto_tecnico": "Quantidade de contratos permitida excedida.",
    },
    282: {
        "codigo": 282,
        "texto_tecnico": "Beneficio não pertence ao Banco informado.",
    },
    283: {
        "codigo": 283,
        "texto_tecnico": "Início do desconto informado já ultrapassado.",
    },
    284: {
        "codigo": 284,
        "texto_tecnico": "Número da parcela inválida.",
    },
    285: {
        "codigo": 285,
        "texto_tecnico": "Quantidade de parcela inválida.",
    },
    286: {
        "codigo": 286,
        "texto_tecnico": "Margem consignável excedida para o mutuário dentro do prazo do contrato.",  # noqa
    },
    287: {
        "codigo": 287,
        "texto_tecnico": "Empréstimo já cadastrado.",
    },
    288: {
        "codigo": 288,
        "texto_tecnico": "Empréstimo inexistente.",
    },
    289: {
        "codigo": 289,
        "texto_tecnico": "Empréstimo já encerrado.",
    },
    290: {
        "codigo": 290,
        "texto_tecnico": "Arquivo sem trailer.",
    },
    291: {
        "codigo": 291,
        "texto_tecnico": "Mutuário sem crédito na competência.",
    },
    292: {
        "codigo": 292,
        "texto_tecnico": "Não descontado - outros motivos.",
    },
    293: {
        "codigo": 293,
        "texto_tecnico": "Retorno de Crédito não pago.",
    },
    294: {
        "codigo": 294,
        "texto_tecnico": "Cancelamento de empréstimo retroativo.",
    },
    295: {
        "codigo": 295,
        "texto_tecnico": "Outros Motivos de Glosa.",
    },
    296: {
        "codigo": 296,
        "texto_tecnico": "Margem consignável excedida para o mutuário acima do prazo do contrato.",  # noqa
    },
    297: {
        "codigo": 297,
        "texto_tecnico": "Mutuário desligado do empregador.",
    },
    298: {
        "codigo": 298,
        "texto_tecnico": "Mutuário afastado por licença.",
    },
    299: {
        "codigo": 299,
        "texto_tecnico": "Primeiro nome do mutuário diferente do primeiro nome do movimento do censo ou diferente da base de Titular do Benefício.",  # noqa
    },
    300: {
        "codigo": 300,
        "texto_tecnico": "Benefício suspenso/cessado pela APS ou Sisobi.",
    },
    301: {
        "codigo": 301,
        "texto_tecnico": "Benefício suspenso por dependência de cálculo.",
    },
    302: {
        "codigo": 302,
        "texto_tecnico": "Benefício suspenso/cessado pela inspetoria/auditoria.",
    },
    303: {
        "codigo": 303,
        "texto_tecnico": "Benefício bloqueado para empréstimo pelo beneficiário.",
    },
    304: {
        "codigo": 304,
        "texto_tecnico": "Benefício bloqueado para empréstimo por TBM.",
    },
    305: {
        "codigo": 305,
        "texto_tecnico": "Benefício está em fase de concessão de PA ou desdobramento.",
    },
    306: {
        "codigo": 306,
        "texto_tecnico": "Benefício cessado por óbito.",
    },
    307: {
        "codigo": 307,
        "texto_tecnico": "Benefício cessado por fraude.",
    },
    308: {
        "codigo": 308,
        "texto_tecnico": "Benefício cessado por concessão de outro benefício.",
    },
    309: {
        "codigo": 309,
        "texto_tecnico": "Benefício cessado: estatutário transferido para órgão de origem.",  # noqa
    },
    310: {
        "codigo": 310,
        "texto_tecnico": "Empréstimo suspenso pela APS.",
    },
    311: {
        "codigo": 311,
        "texto_tecnico": "Empréstimo cancelado pelo banco.",
    },
    312: {
        "codigo": 312,
        "texto_tecnico": "Crédito transformado em PAB.",
    },
    313: {
        "codigo": 313,
        "texto_tecnico": "Término da consignação foi alterado.",
    },
    314: {
        "codigo": 314,
        "texto_tecnico": "Fim do empréstimo ocorreu durante período de suspensão ou concessão.",  # noqa
    },
    315: {
        "codigo": 315,
        "texto_tecnico": "Empréstimo suspenso pelo banco.",
    },
    316: {
        "codigo": 316,
        "texto_tecnico": "Não averbação de contrato - quantidade de parcelas/competências informadas ultrapassou a data limite da extinção de cota do dependente titular de benefícios.",  # noqa
    },
    317: {
        "codigo": 317,
        "texto_tecnico": "Lote Não Aceito - Totais do Lote com Diferença.",
    },
    318: {
        "codigo": 318,
        "texto_tecnico": "Título Não Encontrado.",
    },
    319: {
        "codigo": 319,
        "texto_tecnico": "Identificador Registro Opcional Inválido.",
    },
    320: {
        "codigo": 320,
        "texto_tecnico": "Código Padrão Inválido.",
    },
    321: {
        "codigo": 321,
        "texto_tecnico": "Código de Ocorrência Inválido.",
    },
    322: {
        "codigo": 322,
        "texto_tecnico": "Complemento de Ocorrência Inválido.",
    },
    323: {
        "codigo": 323,
        "texto_tecnico": "Alegação já Informada.",
    },
    324: {
        "codigo": 324,
        "texto_tecnico": "Agência/Conta do Favorecido Substituída.",
    },
    325: {
        "codigo": 325,
        "texto_tecnico": "Divergência entre o primeiro e último nome do beneficiário versus primeiro e último nome na Receita Federal.",  # noqa
    },
    326: {
        "codigo": 326,
        "texto_tecnico": "Confirmação de Antecipação de Valor.",
    },
    327: {
        "codigo": 327,
        "texto_tecnico": "Antecipação parcial de valor.",
    },
    328: {
        "codigo": 328,
        "texto_tecnico": "Boleto bloqueado na base. Não passível de pagamento.",
    },
    329: {
        "codigo": 329,
        "texto_tecnico": "Sistema em contingência - Boleto valor maior que referência.",
    },
    330: {
        "codigo": 330,
        "texto_tecnico": "Sistema em contingência - Boleto vencido.",
    },
    331: {
        "codigo": 331,
        "texto_tecnico": "Sistema em contingência - Boleto indexado.",
    },
    332: {
        "codigo": 332,
        "texto_tecnico": "Beneficiário divergente.",
    },
    333: {
        "codigo": 333,
        "texto_tecnico": "Limite de pagamentos parciais do boleto excedido. Consulte o Beneficiário do boleto.",  # noqa
    },
    334: {
        "codigo": 334,
        "texto_tecnico": "Boleto já liquidado. Não passível de pagamento.",
    },
    335: {
        "codigo": 335,
        "texto_tecnico": "PIX não efetivado.",
    },
    336: {
        "codigo": 336,
        "texto_tecnico": "Transação interrompida devido a erro no PSP do Recebedor.",
    },
    337: {
        "codigo": 337,
        "texto_tecnico": "Número da conta transacional encerrada no PSP do Recebedor.",
    },
    338: {
        "codigo": 338,
        "texto_tecnico": "Tipo incorreto para a conta transacional especificada.",
    },
    339: {
        "codigo": 339,
        "texto_tecnico": "Tipo de transação não é suportado/autorizado na conta transacional especificada.",  # noqa
    },
    340: {
        "codigo": 340,
        "texto_tecnico": "CPF/CNPJ do usuário recebedor não é consistente com o titular da conta transacional especificada.",  # noqa
    },
    341: {
        "codigo": 341,
        "texto_tecnico": "CPF/CNPJ do usuário recebedor incorreto.",
    },
    342: {
        "codigo": 342,
        "texto_tecnico": "Ordem rejeitada pelo PSP do Recebedor.",
    },
    343: {
        "codigo": 343,
        "texto_tecnico": "ISPB do PSP do Pagador inválido ou inexistente.",
    },
    344: {
        "codigo": 344,
        "texto_tecnico": "Chave não cadastrada no DICT.",
    },
    345: {
        "codigo": 345,
        "texto_tecnico": "QR Code inválido/vencido.",
    },
    346: {
        "codigo": 346,
        "texto_tecnico": "Forma de iniciação inválida.",
    },
    347: {
        "codigo": 347,
        "texto_tecnico": "Chave de pagamento inválida.",
    },
    348: {
        "codigo": 348,
        "texto_tecnico": "Chave de pagamento não informada.",
    },
    999: {
        "codigo": 999,
        "texto_tecnico": "Consultar o Banco para detalhar o erro.",
    },
}

ERROS_ESTORNO_PAGAMENTO_DICT = {
    1: "Conta destinatária do crédito encerrada",
    2: "Agência ou conta destinatária do crédito inválida",
    3: "Ausência ou divergência na indicação do CPF/CNPJ",
    4: "Mensagem inválida para o tipo de transação ou finalidade",
    5: "Divergência na titularidade",
    6: "Transferência insuficiente para finalidade indicada",
    7: "Diferença a maior",
    8: "Código identificador de transferência inválido",
    9: "Devolução por fraude",
    15: "Identificação Depósito Judicial inválida",
    16: "Mensagem STRO020/PAG0116 fora do horário definido do negócio",
    17: "Número de contrato inválido",
    18: "Valor em duplicidade",
    19: "Movimentações finceiras ligadas ao terrorismo e seu financiamento",
    22: "Devolução de ordem bancária pelo agente financeiro",
    24: "Erro no Preenchimento do Documento de Recolhimento",
    25: "Erro no Preenchimento do Depósito Direto",
    26: "Devolução de pagamento de tributos por solicitação da IF",
    27: "Devolução de recolhimento a maior autorizada pela Receita Federal do Brasil",
    28: "Crédito não sacado - decurso de prazo estipulado",
    31: "CPF/CNPJ inapto junto a Receita Federal do Brasil",
    61: "Transferência supera limite para o tipo de conta destino",
    70: "Por solicitação de cliente da Inst Partcpt Receb",
    72: "Não conformidade no pagamento",
    84: "Conta destino inválida para o tipo de transferência",
}
