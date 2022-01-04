import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper()

end_to_end_id = "E000000002020111014304601145319A"

response = c.consultar_pix(end_to_end_id)

dump_response(response, os.path.realpath(__file__))
