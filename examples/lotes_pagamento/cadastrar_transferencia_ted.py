import os
from datetime import date

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))


today = date.today()
bb_fmt = "%d%m%Y"

lote_data = {
    "n_requisicao": 579144,
    "agencia": 1607,
    "conta": 99738672,
    "dv_conta": "X",
}
transferencia_data = {
    "codigo_banco": 1,
    "agencia_destino": 18,
    "conta_destino": 3066,
    "dv_conta_destino": "X",
    "documento": "99391916180",
    "data_transferencia": today.strftime(bb_fmt),
    "valor_transferencia": 15.50,
    "descricao": "string",
    "finalidade_ted": 1,
}


response = c.cadastrar_transferencia(**lote_data, **transferencia_data)

dump_response(response, os.path.realpath(__file__))
