import os
from datetime import date

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))


today = date.today()
bb_fmt = "%d%m%Y"


lote_data = {
    "n_requisicao": 11489,
    "agencia": 1607,
    "conta": 99738672,
    "dv_conta": "X",
}

transferencia_data = {
    "data_transferencia": today.strftime(bb_fmt),
    "valor_transferencia": 15.50,
    "descricao": "Uma transferência via dados bancários",
    "tipo_conta_favorecido": 1,
    "agencia_favorecido": 1234,
    "conta_favorecido": 12345,
    "digito_verificador_conta": "X",
    "documento": "28779295827",
}

response = c.criar_transferencia_por_dados_bancarios_pix(
    **lote_data, **transferencia_data
)
dump_response(response, os.path.realpath(__file__))
