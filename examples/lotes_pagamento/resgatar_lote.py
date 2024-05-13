import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper
import logging

logging.basicConfig(level=logging.DEBUG)

c = PagamentoLoteBBWrapper(
    cert=("./certs/imobanco_cert.pem", "./certs/imobanco_key.pem")
)

_id = "9999988"

response = c.resgatar_lote(
    _id,
)
print(response.data)

dump_response(response, os.path.realpath(__file__))
