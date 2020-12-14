from decouple import config


IS_SANDBOX = config("IMOBANCO_BB_IS_SANDBOX", default=True)
"""É ambiente de teste?"""

BASIC_TOKEN = config("IMOBANCO_BB_BASIC_TOKEN", default=True)
"""Token básico para autenticação"""

GW_APP_KEY = config("IMOBANCO_BB_GW_APP_KEY", default=True)
"""developer_application_key"""

CONVENIO_NUMBER = config("IMOBANCO_BB_CONVENIO_NUMBER", default=True)
"""número do convênio"""
