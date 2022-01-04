import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper()

_id = '97310300051430001'


response = c.consultar_transferencia(
    _id,
)

dump_response(response, os.path.realpath(__file__))
