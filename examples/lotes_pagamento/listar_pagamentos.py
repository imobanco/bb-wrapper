import os
from datetime import date

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))

inicio = date(2022, 2, 8)
fim = date(2022, 2, 11)
bb_fmt = "%d%m%Y"

response = c.listar_pagamentos(
    inicio=inicio.strftime(bb_fmt), fim=fim.strftime(bb_fmt), index=0
)

dump_response(response, os.path.realpath(__file__))
