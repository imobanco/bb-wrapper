import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))

_id = "97310305791490001"


response = c.consultar_pagamento_tributo(
    _id,
)

dump_response(response, os.path.realpath(__file__))
