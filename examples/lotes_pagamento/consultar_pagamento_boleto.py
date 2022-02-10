import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper()

_id = "92764700000030001"


response = c.consultar_pagamento_boleto(
    _id,
)

dump_response(response, os.path.realpath(__file__))
