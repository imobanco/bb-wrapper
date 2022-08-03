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
    1: "Agência de crédito igual a zero. Informe o número da Agência de Crédito.",
    2: "Conta de crédito não é numérica. Informe apenas números.",
    3: "Dígito conta de crédito igual a espaços. Informe o DV da conta de crédito.",
    4: "CPF não é numérico. Informe apenas números.",
    5: "CNPJ não é numérico. Informe apenas números.",
    6: "Data do pagamento igual a zeros. Informe a data do pagamento.",
    7: "Data do pagamento inválida. Informe uma data de pagamento válida.",
    8: "Valor do pagamento não é númerico. Informe apenas números.",
    9: "Valor do pagamento igual a zeros. Informe o valor do pagamento.",
    10: "Ambos os campos Número Compensação e Número ISPB estão zerados.",
    11: "Ambos os campos Número Compensação e Número ISPB foram informados.",
    12: "Ambos os campos Finalidade DOC e Finalidade TED estão zerados.",
    13: "Ambos os campos Finalidade DOC e Finalidade TED foram informados.",
    14: "Número depósito judicial igual a espaços.",
    15: "Dígito da conta de crédito inválido.",
    16: "Ambos os campos CPF e CNPJ foram informados. Informe apenas um dos campos.",
    17: "Ambos os campos CPF e CNPJ estão zerados. Informe um dos campos.",
    18: "Dígito do CPF inválido. Verifique o dado informado.",
    19: "Dígito do CNPJ inválido. Verifique o dado informado.",
    20: "Agência e conta de crédito estão iguais a de débito. Opção não permitida.",
    21: "Número Compensação inválido. Verifique o dado informado.",
    22: "Número ISPB diferente de zeros. Não informe o número ISPB.",
    23: "Conta de crédito igual a zeros. Informe o número da conta de crédito.",
    24: "CPF igual a zeros. Obrigatório informar o número do CPF.",
    25: "CNPJ diferente de zeros. Não permitido informar CNPJ.",
    26: "Conta de crédito diferente de zeros. Não permitido informar Conta de crédito.",
    27: "Dígito conta de crédito diferente de espaços. Não informar dígito da conta de crédito.",  # noqa
    28: "Finalidade DOC diferente de zeros. Não informar finalidade DOC.",
    29: "Finalidade TED diferente de zeros. Não informar finalidade TED.",
    30: "Número Depósito Judicial diferente de espaços. Não informar finalidade Depósito Judicial.",  # noqa
    31: "Número do documento de crédito não é numérico. Informar números.",
    32: "Número do documento de débito não é numérico. Informar números.",
    33: "CPF não encontrado na base da receita federal",
    34: "CNPJ não encontrado na base da receita federal",
    35: "Conta de poupança não permitido.",
    36: "Código COMPE deve ser igual a 1",
    37: "Código ISPB deve ser igual a 0",
    38: "Código de barras não é numérico. Informar números.",
    39: "Código de barras igual a zeros. Informar números.",
    40: "Número de inscrição do pagador não é numérico. Informar números.",
    41: "Número de inscrição do beneficiário não é numérico. Informar números.",
    42: "Número de inscrição do avalista não é numérico. Informar números.",
    43: "Dígito do CPF para o pagador inválido. Verifique o número correto.",
    44: "Dígito do CPF para o beneficiário inválido. Verifique o número correto.",
    45: "Dígito do CPF para o avalista inválido. Verifique o número correto.",
    46: "Dígito do CNPJ para o pagador inválido. Verifique o número correto.",
    47: "Dígito do CNPJ para o beneficiário inválido. Verifique o número correto.",
    48: "Dígito do CNPJ para o avalista inválido. Verifique o número correto.",
    49: "Data do vencimento inválida.  Informar data válida.",
    50: "Valor nominal não é numérico. Informar números.",
    51: "Valor de desconto não é numérico. Informar números.",
    52: "Valor de mora não é numérico. Informar números.",
    53: "Data do pagamento deve ser maior ou igual ao dia atual.",
    54: "Número do documento de débito igual a zeros",
    55: "Data do vencimento igual a zeros. Informar data de vencimento.",
    56: "Nome do beneficiário não informado",
    57: "Número de inscrição (CPF/CNPJ) do beneficiário não informado.",
    58: "Conta pagamento diferente de espaços. Não informar conta pagamento.",
    59: "Ambos os campos conta de crédito e conta pagamento foram informados.",
    60: "Transação cancelada pelo cliente",
    61: "Código da Receita do Tributo não informado",
    62: "Tipo de Identificação do Contribuinte não informado",
    63: "Número de Identificação do Contribuinte não informado",
    64: "Número de Identificação do Contribuinte não numérico",
    65: "Código de Identificação do Tributo não informado",
    66: "Período de apuração não informado",
    67: "Número de Referência não informado",
    68: "Valor Principal não é numérico",
    69: "Valor Principal não informado",
    70: "Valor da Multa não é numérico",
    71: "Valor dos Juros/Encargos não é numérico",
    72: "Data de Vencimento não informada",
    73: "Mês e ano de competência não informados",
    74: "Valor previsto do pagamento do INSS não é numérico",
    75: "Valor previsto do pagamento do INSS não informado",
    76: "Valor de Outras Entidades não é numérico",
    77: "Valor de Atualização Monetária não é numérico",
    78: "Valor de Atualização Monetária não é numérico",
    79: "Período de apuração inválido",
    80: "Conta de crédito inválida. Informe o número sem o 45 do início.",
    81: "A conta informada não pertence ao funcionário.",
    82: "Pagamento permitido apenas para pessoas físicas.",
    83: "Agência e Conta incorretos.",
    84: "A conta informada não está ativa.",
    85: "Conta não permite crédito de salário. Informe outra conta.",
    86: "Ambos os campos agência de crédito e conta pagamento foram informados",
    90: "Mês de competência inválido",
    91: "Valor de outras deduções inválido",
    92: "Valor de outros acréscimos inválido",
    93: "Código da forma de identificação do cliente não foi informado",
    94: "DDD do cliente do PIX não foi informado",
    95: "Telefone do Cliente do PIX não foi informado",
    96: "Email do cliente do PIX não foi informado",
    97: "Chave Aleatória do Cliente do PIX não foi informado",
    98: "Código de tipo de conta do Cliente do PIX não foi informado",
    99: "Consultar o Banco para detalhar o erro",
    100: "E-mail inválido",
    101: "Email do cliente do PIX não deve conter caractere especial",
    102: "Telefone Inválido",
    103: "DDD inválido",
    104: "E-mail com tamanho maior que 77 caracteres.",
    105: "Conta de crédito inválida. Informe um número de conta válido.",
    106: "CPF inválido. Informe um CPF válido.",
    107: "CNPJ inválido. Informe um CNPJ válido.",
    108: "Número do documento de crédito inválido. Informe um número válido.",
    109: "Número do documento de débito inválido. Informe um número válido.",
    110: "Valor do pagamento inválido. Informe um valor válido.",
    111: "Valor nominal inválido. Informe um valor válido.",
    112: "Valor de desconto inválido. Informe um valor válido.",
    113: "Valor de mora inválido. Informe um valor válido.",
    114: "Número de inscrição do beneficiário inválido. Informe um número válido.",
    115: "Número de inscrição do pagador inválido. Informe um número válido.",
    116: "Número de inscrição do avalista inválido. Informe um número válido.",
    117: "Número de identifiação do contribuinte DARF inválido. Informe um número válido.",  # noqa
    118: "Número de referência inválido. Informe um número válido.",
    119: "Valor principal inválido. Informe um valor válido.",
    120: "Valor da multa inválido. Informe um valor válido.",
    121: "Valor dos juros/encargos inválido. Informe um valor válido.",
    122: "Número de identificação do contribuinte GPS inválido. Informe um número válido.",  # noqa
    123: "Valor previsto do pagamento do INSS inválido. Informe um valor válido.",
    124: "Valor de outras entidades inválido. Informe um valor válido.",
    125: "Valor de atualização monetária inválido. Informe um valor válido.",
    126: "Valor de desconto GRU inválido. Informe um valor válido.",
    200: "Insuficiência de Fundos - Débito Não Efetuado",
    201: "Crédito ou Débito Cancelado pelo Pagador",
    202: "Débito Autorizado pela Agência - Efetuado",
    203: "Controle Inválido. Verificar campos do Arquivo CNAB240.",
    204: "Tipo de Operação Inválido.",
    205: "Tipo de Serviço Inválido.",
    206: "Forma de Lançamento Inválida.",
    207: "Tipo/Número de Inscrição Inválido. CPF ou CNPJ inválido.",
    208: "Código de Convênio Inválido",
    209: "Agência/Conta Corrente/DV Inválido",
    210: "Número Sequencial do Registro no Lote Inválido",
    211: "Código de Segmento de Detalhe Inválido",
    212: "Lançamento inconsistente.",
    213: "Número Compe do Banco para crédito Inválido",
    214: "Número do ISPB Banco, Instituição de Pagamento para crédito Inválido",
    215: "Agência Mantenedora da Conta Corrente do Favorecido Inválida",
    216: "Conta Corrente/DV/Conta de Pagamento do Favorecido Inválido",
    217: "Nome do Favorecido Não Informado",
    218: "Data Lançamento Inválida",
    219: "Tipo/Quantidade da Moeda Inválido",
    220: "Valor do Lançamento Inválido",
    221: "Aviso ao Favorecido - Identificação Inválida",
    222: "Tipo/Número de Inscrição (CPF/CNPJ) do Favorecido Inválido.",
    223: "Logradouro do Favorecido Não Informado",
    224: "Número do Local do Favorecido Não Informado",
    225: "Cidade do Favorecido Não Informada",
    226: "CEP/Complemento do Favorecido Inválido",
    227: "Sigla do Estado do Favorecido Inválida",
    228: "Número do Banco para crédito Inválido",
    229: "Código/Nome da Agência Depositária Não Informado",
    230: "Seu Número Inválido",
    231: "Nosso Número Inválido",
    232: "Inclusão Efetuada com Sucesso",
    233: "Alteração Efetuada com Sucesso",
    234: "Exclusão Efetuada com Sucesso",
    235: "Agência/Conta Impedida Legalmente",
    236: "Empresa não pagou salário. Conta de crédito só aceita pagamento de salário",
    237: "Falecimento do mutuário",
    238: "Empresa não enviou remessa do mutuário",
    239: "Empresa não enviou remessa no vencimento",
    240: "Valor da parcela inválida",
    241: "Identificação do contrato inválida",
    242: "Operação de Consignação Incluída com Sucesso",
    243: "Operação de Consignação Alterada com Sucesso",
    244: "Operação de Consignação Excluída com Sucesso",
    245: "Operação de Consignação Liquidada com Sucesso",
    246: "Reativação Efetuada com Sucesso",
    247: "Suspensão Efetuada com Sucesso",
    248: "Código de Barras - Código do Banco Inválido",
    249: "Código de Barras - Código da Moeda Inválido",
    250: "Código de Barras - Dígito Verificador Geral Inválido",
    251: "Código de Barras - Valor do Título Inválido",
    252: "Código de Barras - Campo Livre Inválido",
    253: "Valor do Documento Inválido",
    254: "Valor do Abatimento Inválido",
    255: "Valor do Desconto Inválido",
    256: "Valor de Mora Inválido",
    257: "Valor da Multa Inválido",
    258: "Valor do IR Inválido",
    259: "Valor do ISS Inválido",
    260: "Valor do IOF Inválido",
    261: "Valor de Outras Deduções Inválido",
    262: "Valor de Outros Acréscimos Inválido",
    263: "Valor do INSS Inválido",
    264: "Lote Não Aceito",
    265: "Inscrição da Empresa Inválida para o Contrato",
    266: "Convênio com a Empresa Inexistente/Inválido para o Contrato",
    267: "Agência/Conta Corrente da Empresa Inexistente/Inválido para o Contrato",
    268: "Tipo de Serviço Inválido para o Contrato",
    269: "Conta Corrente da Empresa com Saldo Insuficiente",
    270: "Lote de Serviço Fora de Sequência",
    271: "Lote de Serviço Inválido",
    272: "Arquivo não aceito",
    273: "Tipo de Registro Inválido",
    274: "Código Remessa / Retorno Inválido",
    275: "Versão de layout inválida",
    276: "Mutuário não identificado",
    277: "Tipo do beneficio não permite empréstimo",
    278: "Beneficio cessado/suspenso",
    279: "Beneficio possui representante legal",
    280: "Beneficio é do tipo PA (Pensão alimentícia)",
    281: "Quantidade de contratos permitida excedida",
    282: "Beneficio não pertence ao Banco informado",
    283: "Início do desconto informado já ultrapassado",
    284: "Número da parcela inválida",
    285: "Quantidade de parcela inválida",
    286: "Margem consignável excedida para o mutuário dentro do prazo do contrato",
    287: "Empréstimo já cadastrado",
    288: "Empréstimo inexistente",
    289: "Empréstimo já encerrado",
    290: "Arquivo sem trailer",
    291: "Mutuário sem crédito na competência",
    292: "Não descontado – outros motivos",
    293: "Retorno de Crédito não pago",
    294: "Cancelamento de empréstimo retroativo",
    295: "Outros Motivos de Glosa",
    296: "Margem consignável excedida para o mutuário acima do prazo do contrato",
    297: "Mutuário desligado do empregador",
    298: "Mutuário afastado por licença",
    299: "Primeiro nome do mutuário diferente do primeiro nome do movimento",
    300: "Benefício suspenso/cessado pela APS ou Sisobi",
    301: "Benefício suspenso por dependência de cálculo",
    302: "Benefício suspenso/cessado pela inspetoria/auditoria",
    303: "Benefício bloqueado para empréstimo pelo beneficiário",
    305: "Benefício está em fase de concessão de PA ou desdobramento",
    304: "Benefício bloqueado para empréstimo por TBM",
    306: "Benefício cessado por óbito",
    307: "Benefício cessado por fraude",
    308: "Benefício cessado por concessão de outro benefício",
    309: "Benefício cessado: estatutário transferido para órgão de origem",
    310: "Empréstimo suspenso pela APS",
    311: "Empréstimo cancelado pelo banco",
    312: "Crédito transformado em PAB",
    313: "Término da consignação foi alterado",
    314: "Fim do empréstimo ocorreu durante período de suspensão ou concessão",
    315: "Empréstimo suspenso pelo banco",
    316: "Não averbação de contrato",
    317: "Lote Não Aceito - Totais do Lote com Diferença",
    318: "Título Não Encontrado",
    319: "Identificador Registro Opcional Inválido",
    320: "Código Padrão Inválido",
    321: "Código de Ocorrência Inválido",
    322: "Complemento de Ocorrência Inválido",
    323: "Alegação já Informada",
    324: "Agência / Conta do Favorecido Substituída",
    325: "Divergência entre o primeiro e último nome do beneficiário na Receita Federal",  # noqa
    326: "Confirmação de Antecipação de Valor",
    327: "Antecipação parcial de valor",
    328: "Boleto bloqueado na base. Não passível de pagamento.",
    329: "Sistema em contingência – Boleto valor maior que referência",
    330: "Sistema em contingência – Boleto vencido",
    331: "Sistema em contingência – Boleto indexado",
    332: "Beneficiário divergente.",
    333: "Limite de pagamentos parciais do boleto excedido.",
    334: "Boleto já liquidado. Não passível de pagamento.",
    999: "Consultar o Banco para detalhar o erro",
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
