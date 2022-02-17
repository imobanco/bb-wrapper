import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper()

end_to_end_id = "E00000000202101081802KEP4RED55RB"
txid = "?"

response = c.devolver_pix(end_to_end_id, "0.01", txid)

dump_response(response, os.path.realpath(__file__))
