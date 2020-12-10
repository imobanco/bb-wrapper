from imobanco_bb.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

data = {}

response = wrapper.registra_boleto(data)

print(response.data)
