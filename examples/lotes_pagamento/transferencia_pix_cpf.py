import os
from datetime import date

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))


today = date.today()
bb_fmt = "%d%m%Y"


lote_data = {
    "n_requisicao": 9221347,
    "agencia": 1607,
    "conta": 99738672,
    "dv_conta": "X",
}

transferencia_data = {
    "descricao": "transferencia CPF",
    "data_transferencia": today.strftime(bb_fmt),
    "valor_transferencia":7999.99,
    "forma_id": 3,
    "cpf": "28779295827",
}

response = c.criar_transferencia_pix(**lote_data, **transferencia_data)
dump_response(response, os.path.realpath(__file__))
