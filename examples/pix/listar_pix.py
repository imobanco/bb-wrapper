import os

from examples.utils import dump_response

from bb_wrapper.wrapper.pix import PIXCobBBWrapper

c = PIXCobBBWrapper()

response = c.listar_pix()

dump_response(response, os.path.basename(__file__).split(".")[0])
