import logging
import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

logging.basicConfig(level=logging.DEBUG)

c = PagamentoLoteBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))

_id = "90579174731030001"


response = c.consultar_transferencia(
    _id,
)

dump_response(response, os.path.realpath(__file__))
