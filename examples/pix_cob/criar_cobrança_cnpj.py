import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper()

data = {
    "expiracao": 60 * 60,  # 60 segundos = 1 minuto. 60 minutos = 1h
    "documento_devedor": "14747277000197",
    "nome_devedor": "ÉṔçà`s Francisco da Silva Francisco da Silva Francisco da Silva Francisco da Silva Francisco da Silva",  # noqa: E501
    "valor": 130.44,
    "nome_recebedor": "Imobanco",
    "chave": "7f6844d0-de89-47e5-9ef7-e0a35a681615",
    "descricao": "Cobrança dos serviços prestados.",
    "info": [{"nome": "Sacado", "valor": "Nome do sacado aqui"}],
}

response = c.criar_cobranca(**data)

dump_response(response, os.path.basename(__file__).split(".")[0])
