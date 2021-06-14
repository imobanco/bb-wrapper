import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper()

txid = "QtRnksK1N6Hn6xJgRXWuUn7XGx3TdwErWoK"

response = c.consultar_cobranca(txid)

dump_response(response, os.path.basename(__file__).split(".")[0])
