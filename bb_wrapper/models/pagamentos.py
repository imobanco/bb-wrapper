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

ERROS_PAGAMENTO_DICT = {
    1: "Agência de crédito está zerada. Informe o nº da Agência de Crédito.",
    2: "Conta de crédito informada não é numérica. Informe apenas números.",
    3: "Dígito da conta de crédito não informado. Informe o DV da conta de crédito.",
    4: "CPF informado não é numérico. Informe apenas números.",
    5: "CNPJ informado não é numérico. Informe apenas números.",
    6: "Data do pagamento não informada. Informe a data do pagamento.",
    7: "Data do pagamento inválida. Verifique o dado informado.",
    8: "Valor do pagamento informado não é númerico. Informe apenas números.",
    9: "Valor do pagamento está zerado. Informe o valor do pagamento.",
    10: "Ambos os campos Número Compensação e Número ISPB não foram informados. Informe um dos campos.",  # noqa: E501
    11: "Ambos os campos Número Compensação e Número ISPB foram informados. Informe apenas um dos campos.",  # noqa: E501
    12: "Ambos os campos Finalidade DOC e Finalidade TED não foram informados. Informe um dos campos.",  # noqa: E501
    13: "Ambos os campos Finalidade DOC e Finalidade TED foram informados. Informe apenas um dos campos.",  # noqa: E501
    14: "Número de depósito judicial não informado. Informe o número do depósito judicial.",  # noqa: E501
    15: "Digito da conta de crédito inválido. Verifique o dado informado.",
    16: "Ambos os campos CPF e CNPJ foram informados. Informe apenas um dos campos. Caso informado os 2 campos, nas consultas será exibido apenas os dados do CPF.",  # noqa: E501
    17: "Ambos os campos CPF e CNPJ não foram informados. Informe um dos campos.",
    18: "Dígito do CPF inválido. Verifique o dado informado.",
    19: "Dígito do CNPJ inválido. Verifique o dado informado.",
    20: "Agência e conta de crédito estão iguais às de débito. Opção não permitida.",
    21: "Número Compensação inválido. Verifique o dado informado.",
    22: "Número ISPB diferente de zeros. Não informe o nº ISPB.",
    23: "Conta de crédito não informada. Informe o número da conta de crédito.",
    24: "CPF não informado. Informe o nº do CPF.",
    25: "CNPJ foi informado. Não informe CNPJ.",
    26: "Conta de crédito foi informada. Não informe Conta de crédito.",
    27: "Dígito da conta de crédito foi informado. Não informe dígito da conta de crédito.",  # noqa: E501
    28: "Finalidade do DOC foi informada. Não informe finalidade do DOC.",
    29: "Finalidade da TED foi informada. Não informe finalidade da TED.",
    30: "Número Depósito Judicial informado. Não informe finalidade Depósito Judicial.",
    31: "Número do documento de crédito informado não é numérico. Informe apenas números.",  # noqa: E501
    32: "Número do documento de débito não é numérico. Informe apenas números.",
    33: "CPF não encontrado na base da receita federal. Verifique o dado informado.",
    34: "CNPJ não encontrado na base da receita federal. Verifique o dado informado.",
    35: "Conta poupança não permitido para 'Pagamento ao Fornecedor'. Para creditar em conta poupança utilize o recurso para efetivação de 'Pagamentos Diversos'.",  # noqa: E501
    36: "Código COMPE deve ser igual a 1",
    37: "Código ISPB deve ser igual a 0",
    38: "Código de barras não é numérico. Informe apenas números.",
    39: "Código de barras igual a zeros. Informe apenas números.",
    40: "Número de inscrição do pagador não é numérico. Informe apenas números.",
    41: "Número de inscrição do beneficiário não é numérico. Informe apenas números.",
    42: "Número de inscrição do avalista não é numérico. Informe apenas números.",
    43: "Digito do CPF para o pagador inválido. Verifique o dado informado.",
    44: "Digito do CPF para o beneficiário inválido. Verifique o dado informado.",
    45: "Digito do CPF para o avalista inválido. Verifique o dado informado.",
    46: "Digito do CNPJ para o pagador inválido. Verifique o dado informado.",
    47: "Digito do CNPJ para o beneficiário inválido. Verifique o dado informado.",
    48: "Digito do CNPJ para o avalista inválido.Verifique o dado informado.",
    49: "Data do vencimento inválida. Verifique o dado informado.",
    50: "Valor nominal não é numérico. Informe apenas números.",
    51: "Valor de desconto não é numérico. Informe apenas números;",
    52: "Valor de mora não é numérico. Informe apenas números.",
    53: "Data do pagamento deve ser maior ou igual ao dia atual.",
    54: "Número do documento de débito não informado. Informe o nº do doc de débito.",
    55: "Data do vencimento não informada. Informe a data de vencimento.",
    56: "Nome do beneficiário não informado. Informe o nome do beneficiário.",
    57: "Número de inscrição do beneficiário não informado. Informe o CPF ou o CNPJ do beneficiário.",  # noqa: E501
    58: "Conta pagamento foi informada. Não informe conta pagamento.",
    59: "Ambos os campos conta de crédito e conta pagamento foram informados. Informe apenas um dos campos.",  # noqa: E501
    99: "Consultar o Banco para detalhar o erro",
    200: "Insuficiência de Fundos: Débito Não Efetuado",
    201: "Crédito ou Débito Cancelado pelo Pagador",
    202: "Débito Autorizado pela Agência: Efetuado",
    203: "Controle Inválido. Verificar campos 01, 02 e 03 do header ou segmento A, B, C, J, J52, N, O ou W do Arquivo CNAB240.",  # noqa: E501
    204: "Tipo de Operação Inválido. Verificar campo 04.1 do header de lote. Valor default = C",  # noqa: E501
    205: "Tipo de Serviço Inválido. Utilize 20 para Pagamento a Fornecedores, 30 Pagamento de Salários ou 98 Pagamentos Diversos no header de Lote, campo 05.1, do CNAB240",  # noqa: E501
    206: "Forma de Lançamento Inválida. Para crédito em Poupança utilize Pagamentos Diversos. Para crédito em Conta Pagamento utilize Pagamentos Diversos ou Pagamento a Fornecedores. Para Pagamento de salário a conta de crédito deve ser do BB.",  # noqa: E501
    207: "Tipo/Número de Inscrição Inválido. CPF ou CNPJ inválido. Verifique dados informados.",  # noqa: E501
    208: "Código de Convênio Inválido. Verifique dados informados.",
    209: "Agência/Conta Corrente/DV Inválido. Verifique dados informados.",
    210: "Nº Seqüencial do Registro no Lote Inválido. Verifique dado informado.",
    211: "Código de Segmento de Detalhe Inválido. Verifique dado informado.",
    212: "Lançamento inconsistente, rejeitado na prévia. Corrigir os dados do lançamento e enviar novo pagamento.",  # noqa: E501
    213: "Nº Compe do Banco para crédito Inválido. Verifique dado informado.",
    214: "Nº do ISPB Banco, Instituição de Pagamento para crédito Inválido. Verifique dado informado.",  # noqa: E501
    215: "Agência Mantenedora da Conta Corrente do Favorecido Inválida. Verifique dado informado.",  # noqa: E501
    216: "Conta Corrente/DV/Conta de Pagamento do Favorecido Inválido. Verifique dado informado.",  # noqa: E501
    217: "Nome do Favorecido não Informado. Informe o nome do favorecido.",
    218: "Data Lançamento Inválido. Verifique dado informado.",
    219: "Tipo/Quantidade da Moeda Inválido. Verifique dado informado.",
    220: "Valor do Lançamento Inválido. Verifique dado informado.",
    221: "Aviso ao Favorecido: Identificação Inválida.",
    222: "Tipo/Número de Inscrição do Favorecido Inválido CPF ou CNPJ do favorecido inválido. Arquivo: Verifique o campo 07.3B: registro detalhe do segmento B.",  # noqa: E501
    223: "Logradouro do Favorecido não Informado. Informe o logradouro do favorecido.",
    224: "Nº do Local do Favorecido não Informado. Informe o nº do local do favorecido.",  # noqa: E501
    225: "Cidade do Favorecido não Informada. Informe a cidade do favorecido.",
    226: "CEP/Complemento do Favorecido Inválido. Verifique dado informado.",
    227: "Sigla do Estado do Favorecido Inválida. Verifique dado informado.",
    228: "Nº do Banco para crédito Inválido. Verifique dado informado.",
    229: "Código/Nome da Agência Depositária não Informado. Informe o dado solicitado.",
    230: "Seu Número Inválido. Verifique dado informado.",
    231: "Nosso Número Inválido. Verifique dado informado.",
    232: "Inclusão Efetuada com Sucesso",
    233: "Alteração Efetuada com Sucesso",
    234: "Exclusão Efetuada com Sucesso",
    235: "Agência/Conta Impedida Legalmente",
    236: "Empresa não pagou salário Conta de crédito só aceita pagamento de salário.",
    237: "Falecimento do mutuário.",
    238: "Empresa não enviou remessa do mutuário",
    239: "Empresa não enviou remessa no vencimento",
    240: "Valor da parcela inválida. Verifique dado informado.",
    241: "Identificação do contrato inválida. Verifique dado informado.",
    242: "Operação de Consignação Incluída com Sucesso",
    243: "Operação de Consignação Alterada com Sucesso",
    244: "Operação de Consignação Excluída com Sucesso",
    245: "Operação de Consignação Liquidada com Sucesso",
    246: "Reativação Efetuada com Sucesso",
    247: "Suspensão Efetuada com Sucesso",
    248: "Código de Barras: Código do Banco Inválido.",
    249: "Código de Barras: Código da Moeda Inválido",
    250: "Código de Barras: Dígito Verificador Geral Inválido",
    251: "Código de Barras: Valor do Título Inválido",
    252: "Código de Barras: Campo Livre Inválido",
    253: "Valor do Documento Inválido. Verifique dado informado.",
    254: "Valor do Abatimento Inválido. Verifique dado informado.",
    255: "Valor do Desconto Inválido. Verifique dado informado.",
    256: "Valor de Mora Inválido. Verifique dado informado.",
    257: "Valor da Multa Inválido. Verifique dado informado.",
    258: "Valor do IR Inválido. Verifique dado informado.",
    259: "Valor do ISS Inválido. Verifique dado informado.",
    260: "Valor do IOF Inválido. Verifique dado informado.",
    261: "Valor de Outras Deduções Inválido. Verifique dado informado.",
    262: "Valor de Outros Acréscimos Inválido. Verifique dado informado.",
    263: "Valor do INSS Inválido. Verifique dado informado.",
    264: "Lote Não Aceito. Reenvie os documentos.",
    265: "Inscrição da Empresa Inválida para o Contrato",
    266: "Convênio com a Empresa Inexistente/Inválido para o Contrato",
    267: "Agência/Conta Corrente da Empresa Inexistente/Inválido para o Contrato. Verifique dado informado.",  # noqa: E501
    268: "Tipo de Serviço Inválido para o Contrato. Para contrato de Pagamentos, utilize 20 para Pagamento a Fornecedores, 30 Pagamento de Salários ou 98 Pagamentos Diversos no header de Lote, campo 05.1, do CNAB240",  # noqa: E501
    269: "Conta Corrente da Empresa com Saldo Insuficiente.",
    270: "Lote de Serviço Fora de Seqüência",
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
    284: "Número da parcela inválida. Verifique dado informado.",
    285: "Quantidade de parcela inválida. Verifique dado informado.",
    286: "Margem consignável excedida para o mutuário dentro do prazo do contrato. Verifique suas margens disponíveis.",  # noqa: E501
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
    297: "Mutuário desligado do empregador. Pagamento não permitido.",
    298: "Mutuário afastado por licença. Pagamento não permitido.",
    299: "Primeiro nome do mutuário diferente do primeiro nome do movimento do censo ou diferente da base de Titular do Benefício. Verificar necessidade de ajustes.",  # noqa: E501
    300: "Benefício suspenso/cessado pela APS ou Sisobi",
    301: "Benefício suspenso por dependência de cálculo",
    302: "Benefício suspenso/cessado pela inspetoria/auditoria",
    303: "Benefício bloqueado para empréstimo pelo beneficiário",
    304: "Benefício bloqueado para empréstimo por TBM",
    305: "Benefício está em fase de concessão de PA ou desdobramento.",
    306: "Benefício cessado por óbito.",
    307: "Benefício cessado por fraude.",
    308: "Benefício cessado por concessão de outro benefício.",
    309: "Benefício cessado: estatutário transferido para órgão de origem.",
    310: "Empréstimo suspenso pela APS.",
    311: "Empréstimo cancelado pelo banco.",
    312: "Crédito transformado em PAB.",
    313: "Término da consignação foi alterado.",
    314: "Fim do empréstimo ocorreu durante período de suspensão ou concessão.",
    315: "Empréstimo suspenso pelo banco.",
    316: "Não averbação de contrato – quantidade de parcelas/competências informadas ultrapassou a data limite da extinção de cota do dependente titular de benefícios",  # noqa: E501
    317: "Lote Não Aceito: Totais do Lote com Diferença",
    318: "Título Não Encontrado",
    319: "Identificador Registro Opcional Inválido. Verifique dado informado.",
    320: "Código Padrão Inválido. Verifique dado informado.",
    321: "Código de Ocorrência Inválido. Verifique dado informado.",
    322: "Complemento de Ocorrência Inválido. Verifique dado informado.",
    323: "Alegação já Informada",
    324: "Agência / Conta do Favorecido Substituída. Verifique dado informado.",
    325: "Divergência entre o primeiro e último nome do beneficiário VS primeiro e último nome na Receita Federal. Verificar com beneficiário necessidade de ajustes.",  # noqa: E501
    326: "Confirmação de Antecipação de Valor",
    327: "Antecipação parcial de valor",
    328: "Boleto bloqueado na base. Não passível de pagamento.",
    329: "Sistema em contingência – Boleto valor maior que referência. Consulte o beneficiário ou tente efetuar o pagamento mais tarde.",  # noqa: E501
    330: "Sistema em contingência – Boleto vencido. Consulte o beneficiário ou tente efetuar o pagamento mais tarde.",  # noqa: E501
    331: "Sistema em contingência – Boleto indexado. Consulte o beneficiário ou tente efetuar o pagamento mais tarde.",  # noqa: E501
    332: "Beneficiário divergente. Verifique dado informado.",
    333: "Limite de pagamentos parciais do boleto excedido. Consulte o Beneficiário do boleto.",  # noqa: E501
    334: "Boleto já liquidado. Não passível de pagamento.",
    999: "Consultar o Banco para detalhar o erro.",
}
