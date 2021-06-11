import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper()

data = {
    "expiracao": 60
    * 60
    * 24
    * 90,  # 60 sec = 1 min. 60 min = 1h. 24h = 1 dia. 90 dias = 1 trimestre
    "documento_devedor": "14747277000197",
    "nome_devedor": "Francisco da SilvaFrancisco da SilvaFrancisco da SilvaFrancisco da SilvaFrancisco da Silva",
    "valor": 130.44,
    "nome_recebedor": "Imobanco",
    "chave": "7f6844d0-de89-47e5-9ef7-e0a35a681615",
    "descricao": "Cobrança dos serviços prestados.",
}

response = c.criar_cobranca(**data)

dump_response(response, os.path.basename(__file__).split(".")[0])
