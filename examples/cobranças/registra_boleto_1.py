import os

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

data = wrapper.create_boleto_data_with_defaults(
    {
        "dataEmissao": "07.12.2020",
        "dataVencimento": "07.12.2020",
        "valorOriginal": 100.00,
        "numeroTituloBeneficiario": "0",
        "textoCampoUtilizacaoBeneficiario": "UMA DÍVIDA QUALQUER",
        "numeroTituloCliente": "00031285571231230009",
        "pagador": {
            "tipoRegistro": 1,
            "numeroRegistro": "71128590182",
            "nome": "NOME",
            "endereco": "ENDERECO",
            "cep": "70675727",
            "cidade": "SAO PAULO",
            "bairro": "CENTRO",
            "uf": "SP",
            "telefone": "999939669",
        },
        "email": "cliente@email.com",
    }
)

response = wrapper.registra_boleto(data)

dump_response(response, os.path.basename(__file__).split(".")[0])
