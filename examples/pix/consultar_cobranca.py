import os

from examples.utils import dump_response

from bb_wrapper.wrapper.pix import PIXBBWrapper

c = PIXBBWrapper()

txid = "IxN9HNEA1FSmtcx4FqbR9IH32LjaAfopI0E"

response = c.consultar_cobranca(txid)

dump_response(response, os.path.basename(__file__).split(".")[0])
