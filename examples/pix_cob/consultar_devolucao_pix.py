import os

from examples.utils import dump_response

from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper(cert=("./certs/cert.pem", "./certs/key.pem"))


end_to_end_id = "E000000002021012216250Q5N2JSL8RB"
devolucao_id = "9fc76d58bbda3a0cdd5f1b92b6490216"

response = c.consultar_devolucao_pix(end_to_end_id, devolucao_id)

dump_response(response, os.path.realpath(__file__))
