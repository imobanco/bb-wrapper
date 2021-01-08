import os

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

number = "9999999999"

response = wrapper.baixa_boleto(wrapper.build_our_number(number))

dump_response(response, os.path.basename(__file__).split(".")[0])
