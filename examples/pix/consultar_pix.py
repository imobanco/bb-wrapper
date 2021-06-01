import os

from examples.utils import dump_response

from bb_wrapper.wrapper.pix import PIXBBWrapper

c = PIXBBWrapper()

end_to_end_id = "E000000002020111014304601145319A"

response = c.consultar_pix(end_to_end_id)

dump_response(response, os.path.basename(__file__).split(".")[0])