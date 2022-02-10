import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper()

data = {
    "number": "92764700000020001",
    "convenio": 0,
    "agencia": 2035,
    "conta": 70466,
    "dv_conta": "0",
}


response = c.cancelar_pagamentos(**data)

dump_response(response, os.path.realpath(__file__))
