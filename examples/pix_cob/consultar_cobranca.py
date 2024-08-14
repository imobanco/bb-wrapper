import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))

txid = "6lEZLwT4o1fjmg1BVW3KeIPLc0"

response = c.consultar_cobranca(txid)

dump_response(response, os.path.realpath(__file__))
