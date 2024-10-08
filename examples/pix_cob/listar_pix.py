import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))

response = c.listar_pix(page=0)

dump_response(response, os.path.realpath(__file__))
