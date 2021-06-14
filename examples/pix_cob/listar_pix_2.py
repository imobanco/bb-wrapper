import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper()

response = c.listar_pix(inicio="2020-11-10T00:00:00Z", fim="2020-11-10T23:59:59Z")

dump_response(response, os.path.basename(__file__).split(".")[0])
