import os
from datetime import date

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))


today = date.today()
bb_fmt = "%d%m%Y"


lote_data = {
    "n_requisicao": 13987,
    "agencia": 1607,
    "conta": 99738672,
    "dv_conta": "X",
}

transferencia_data = {
    "descricao": "nova transferencia",
    "data_transferencia": today.strftime(bb_fmt),
    "valor_transferencia": 15.50,
    "chave": "d14d32de-b3b9-4c31-9f89-8df2cec92c50",
}

response = c.criar_transferencia_pix(**lote_data, **transferencia_data)
dump_response(response, os.path.realpath(__file__))
