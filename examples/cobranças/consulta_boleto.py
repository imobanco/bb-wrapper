import os

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

numero = "00031285571231230017"

response = wrapper.consulta_boleto(numero)

dump_response(response, os.path.basename(__file__).split(".")[0])
