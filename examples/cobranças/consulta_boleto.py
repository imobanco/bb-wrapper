import os

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

numero = 9999999986

response = wrapper.consulta_boleto(wrapper.build_our_number(numero))

dump_response(response, os.path.basename(__file__).split(".")[0])
