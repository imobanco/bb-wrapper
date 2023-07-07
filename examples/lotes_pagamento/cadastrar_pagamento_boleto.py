import os
from datetime import date

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))


today = date.today()
bb_fmt = "%d%m%Y"

lote_data = {
    "n_requisicao": 579145,
    "agencia": 1607,
    "conta": 99738672,
    "dv_conta": "X",
}
pagamento_data = {
    "codigo_barras_ou_linha_digitavel": "00196846200000100000000003128557123123000917",
    "documento": "99391916180",
    "data_pagamento": today.strftime(bb_fmt),
    "valor_pagamento": 15.50,
    "valor_nominal": 15.50,
    "descricao": "string",
}


response = c.cadastrar_pagamento_boleto(**lote_data, **pagamento_data)

dump_response(response, os.path.realpath(__file__))
