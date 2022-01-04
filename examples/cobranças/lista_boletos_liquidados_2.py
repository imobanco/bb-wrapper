import os
import datetime

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

past_date = datetime.date.today() - datetime.timedelta(days=10)
bb_fmt = "%d.%m.%Y"

query = {
    "codigoEstadoTituloCobranca": 6,  # liquidados
    "dataInicioMovimento": past_date.strftime(bb_fmt),
}

response = wrapper.lista_boletos(liquidados_flag=True, query=query)

data = response.data

lista_numbers = []
for boleto_data in data["boletos"]:
    lista_numbers.append(int(boleto_data["numeroBoletoBB"][10:]))

print(lista_numbers)

dump_response(response, os.path.realpath(__file__))
