import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PagamentoLoteBBWrapper

c = PagamentoLoteBBWrapper()

data = {}

response = c.criar_transferencia()

dump_response(response, os.path.basename(__file__).split(".")[0])
