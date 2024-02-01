import os
from datetime import date

from examples.utils import dump_response
import logging


from bb_wrapper.wrapper import PagamentoLoteBBWrapper

logging.basicConfig(level=logging.DEBUG)


c = PagamentoLoteBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))


today = date.today()
bb_fmt = "%d%m%Y"


lote_data = {
    "n_requisicao": 9499944,
    "agencia": 1607,
    "conta": 99738672,
    "dv_conta": "X",
}

transferencia_data = {
    "descricao": "transferencia CPF",
    "data_transferencia": today.strftime(bb_fmt),
    "valor_transferencia": 7999.99,
    "chave": "28779295827",
}

response = c.criar_transferencia_por_chave_pix(**lote_data, **transferencia_data)
dump_response(response, os.path.realpath(__file__))
