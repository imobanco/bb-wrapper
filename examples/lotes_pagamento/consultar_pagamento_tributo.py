import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper()

_id = '97310305791470001'


response = c.consultar_pagamento_tributo(
    _id,
)

dump_response(response, os.path.realpath(__file__))
