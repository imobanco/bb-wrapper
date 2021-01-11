import os

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

response = wrapper.lista_boletos(liquidados_flag=False)

dump_response(response, os.path.basename(__file__).split(".")[0])
