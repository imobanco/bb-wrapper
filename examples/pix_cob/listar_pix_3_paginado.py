from bb_wrapper.wrapper import PIXCobBBWrapper

c = PIXCobBBWrapper()

response_1 = c.listar_pix(inicio="2024-08-13T00:00:00Z", fim="2024-08-16T23:59:59Z")
assert response_1.data["parametros"]["paginacao"]["paginaAtual"] == 0

response_2 = c.listar_pix(
    inicio="2024-08-13T00:00:00Z", fim="2024-08-16T23:59:59Z", page=1
)
assert response_2.data["parametros"]["paginacao"]["paginaAtual"] == 1
