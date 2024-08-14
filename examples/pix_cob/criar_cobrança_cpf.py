import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))

data = {
    "expiracao": 60 * 60,  # 60 segundos = 1 minuto. 60 minutos = 1h
    "documento_devedor": "12345678909",
    "nome_devedor": "Francisco da SilvaFrancisco da SilvaFrancisco da SilvaFrancisco da SilvaFrancisco da Silva",  # noqa: E501
    "valor": 130.44,
    "nome_recebedor": "Imobanco",
    "chave": "9e881f18-cc66-4fc7-8f2c-a795dbb2bfc1",
    "descricao": "Cobrança dos serviços prestados.",
    "info": [{"nome": "Sacado", "valor": "Nome do sacado aqui"}],
}

response = c.criar_cobranca(**data)

dump_response(response, os.path.realpath(__file__))
