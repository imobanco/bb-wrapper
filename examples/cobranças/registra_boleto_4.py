import os

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

number = "9999999999"

data = wrapper.create_boleto_data_with_defaults(
    {
        "dataEmissao": "08.01.2021",
        "dataVencimento": "12.01.2021",
        "valorOriginal": 3.0,
        "numeroTituloBeneficiario": number,
        "numeroTituloCliente": wrapper.build_our_number(number),
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
        "avalista": {
            "tipoRegistro": 1,
            "numeroRegistro": "71128590182",
            "nomeRegistro": "NOME",
        },
        "jurosMora": {"tipo": 1, "valor": 0.1},
        "multa": {"tipo": 2, "porcentagem": 0.1, "data": "08.12.2020"},
    }
)

response = wrapper.registra_boleto(data)

dump_response(response, os.path.basename(__file__).split(".")[0])
