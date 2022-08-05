from decouple import config


IS_SANDBOX = config("IMOBANCO_BB_IS_SANDBOX", default=True, cast=bool)
"""É ambiente de teste?"""

BASIC_TOKEN = config("IMOBANCO_BB_BASIC_TOKEN", default="")
"""Token básico para autenticação"""

GW_APP_KEY = config("IMOBANCO_BB_GW_APP_KEY", default="")
"""developer_application_key"""

CONVENIO = config("IMOBANCO_BB_CONVENIO", default="")
"""número do convênio"""

CARTEIRA = config("IMOBANCO_BB_CARTEIRA", default="")
"""número da carteira"""

VARIACAO_CARTEIRA = config("IMOBANCO_BB_VARIACAO_CARTEIRA", default="")
"""número da variação da carteira"""

AGENCIA = config("IMOBANCO_BB_AGENCIA", default="")
"""número da agência"""

CONTA = config("IMOBANCO_BB_CONTA", default="")
"""número da conta"""
