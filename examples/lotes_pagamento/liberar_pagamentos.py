import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper()

number = '5143'


response = c.liberar_pagamentos(
    number
)

dump_response(response, os.path.realpath(__file__))
