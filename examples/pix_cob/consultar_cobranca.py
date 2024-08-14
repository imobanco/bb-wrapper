import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))

txid = "HUAY0i0XMbuq6W3EcGapjsGCp5V19ToaRNR"

response = c.consultar_cobranca(txid)

dump_response(response, os.path.realpath(__file__))
