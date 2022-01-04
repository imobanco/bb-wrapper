import os

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

query = {"codigoEstadoTituloCobranca": 6}  # liquidados

response = wrapper.lista_boletos(liquidados_flag=True, query=query)

data = response.data

lista_numbers = []
for boleto_data in data["boletos"]:
    lista_numbers.append(int(boleto_data["numeroBoletoBB"][10:]))

print(lista_numbers)

dump_response(response, os.path.realpath(__file__))
