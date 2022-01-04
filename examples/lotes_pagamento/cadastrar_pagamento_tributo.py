import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper()

lote_data = {
    "numeroRequisicao": 579147,
    "codigoContrato": 0,
    "numeroAgenciaDebito": 1607,
    "numeroContaCorrenteDebito": 99738672,
    "digitoVerificadorContaCorrenteDebito": "X",
}
pagamento_data = {
    "codigoBarras": "00196846200000100000000003128557123123000917",
    "dataPagamento": '04012022',
    "valorPagamento": 15.50,
}


response = c.cadastrar_pagamento_tributo(lote_data, pagamento_data)

dump_response(response, os.path.realpath(__file__))
