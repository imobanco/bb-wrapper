import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper()

lote_data = {
    "numeroRequisicao": 5140,
    "numeroContratoPagamento": 0,
    "agenciaDebito": 1607,
    "contaCorrenteDebito": 99738672,
    "digitoVerificadorContaCorrente": "X",
    "tipoPagamento": 126,
}
transferencia_data = {
    "data": "21012022",
    "valor": 15.50,
    "chave": '01688745475'
}


response = c.cadastrar_transferencia(lote_data, transferencia_data, pix=True)

dump_response(response, os.path.realpath(__file__))
