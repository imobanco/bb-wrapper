import os

from examples.utils import dump_response

from imobanco_bb.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

numero = "00031285571231230013"

response = wrapper.consulta_boleto(numero)

dump_response(response, os.path.basename(__file__).split(".")[0])
