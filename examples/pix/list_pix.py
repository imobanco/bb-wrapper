import os

from examples.utils import dump_response

from bb_wrapper.wrapper.pix import PIXBBWrapper

c = PIXBBWrapper()

response = c.lista_pix()

dump_response(response, os.path.basename(__file__).split(".")[0])
