import os

from examples.utils import dump_response

from bb_wrapper.wrapper.pix import PIXBBWrapper

c = PIXBBWrapper()

data = {
    "calendario": {
      "expiracao": "36000"
    },
    "devedor": {
      "cpf": "12345678909",
      "nome": "Francisco da Silva"
    },
    "valor": {
      "original": "130.44"
    },
    "chave": "7f6844d0-de89-47e5-9ef7-e0a35a681615",
    "solicitacaoPagador": "Cobrança dos serviços prestados."
}

response = c.criar_cobranca(data)

dump_response(response, os.path.basename(__file__).split(".")[0])
