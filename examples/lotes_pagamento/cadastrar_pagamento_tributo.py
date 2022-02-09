import os
from datetime import date

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper()


today = date.today()
bb_fmt = "%d%m%Y"

lote_data = {
    "numeroRequisicao": 579149,
    "codigoContrato": 0,
    "numeroAgenciaDebito": 1607,
    "numeroContaCorrenteDebito": 99738672,
    "digitoVerificadorContaCorrenteDebito": "X",
}
pagamento_data = {
    "codigoBarras": "85800000000600003282126307082112794112788193",
    "dataPagamento": today.strftime(bb_fmt),
    "valorPagamento": 15.50,
}


response = c.cadastrar_pagamento_tributo(lote_data, pagamento_data)

dump_response(response, os.path.realpath(__file__))
