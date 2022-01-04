import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper()

lote_data = {
    "numeroRequisicao": 5143,
    "numeroContratoPagamento": 0,
    "agenciaDebito": 1607,
    "contaCorrenteDebito": 99738672,
    "digitoVerificadorContaCorrente": "X",
    "tipoPagamento": 126,
}
transferencia_data = {
    "numeroCOMPE": 1,
    # "numeroISPB": 0,
    "agenciaCredito": 18,
    "contaCorrenteCredito": 3066,
    "digitoVerificadorContaCorrente": "X",
    "cpfBeneficiario": 99391916180,
    "dataTransferencia": '04012022',
    "valorTransferencia": 15.50,
    "descricaoTransferencia": "string",
}


response = c.cadastrar_transferencia(lote_data, transferencia_data, pix=False)

dump_response(response, os.path.realpath(__file__))
