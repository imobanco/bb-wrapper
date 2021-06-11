import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper()

txid = "VZOgwPQTBdM94bbpbn2LB2KroSaiGy13PKP"

response = c.consultar_cobranca(txid)

dump_response(response, os.path.basename(__file__).split(".")[0])
