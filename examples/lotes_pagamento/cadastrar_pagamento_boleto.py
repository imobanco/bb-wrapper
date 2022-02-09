import os
from datetime import date

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper()


today = date.today()
bb_fmt = "%d%m%Y"

lote_data = {
    "numeroRequisicao": 579146,
    "codigoContrato": 0,
    "numeroAgenciaDebito": 1607,
    "numeroContaCorrenteDebito": 99738672,
    "digitoVerificadorContaCorrenteDebito": "X",
}
pagamento_data = {
    "numeroCodigoBarras": "00196846200000100000000003128557123123000917",
    "codigoTipoBeneficiario": 1,
    "documentoBeneficiario": 99391916180,
    "dataPagamento": today.strftime(bb_fmt),
    "valorPagamento": 15.50,
    "valorNominal": 15.50,
    "descricaoPagamento": "string",
}


response = c.cadastrar_pagamento_boleto(lote_data, pagamento_data)

dump_response(response, os.path.realpath(__file__))
