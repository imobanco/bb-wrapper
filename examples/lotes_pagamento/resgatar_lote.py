import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))

_id = "579145"  # BOLETO
# _id = "579144"  # TED
# _id = "579143"  # TRIBUTO

response = c.resgatar_lote(
    _id,
)

dump_response(response, os.path.realpath(__file__))
