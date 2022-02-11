import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))

data = {
    "number": "90579175731030001",
    "convenio": 0,
    "agencia": 1607,
    "conta": 99738672,
    "dv_conta": "0",
}


response = c.cancelar_pagamentos(**data)

dump_response(response, os.path.realpath(__file__))
