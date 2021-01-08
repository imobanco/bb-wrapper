import os

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

number = "9999999995"

data = wrapper.create_boleto_data_with_defaults(
    {
        "dataEmissao": "08.01.2021",
        "dataVencimento": "12.01.2021",
        "valorOriginal": 3.0,
        "numeroTituloBeneficiario": number,
        "numeroTituloCliente": wrapper.build_our_number(number),
        "pagador": {
            "tipoInscricao": 1,
            "numeroInscricao": "71128590182",
            "nome": "Nome",
            "endereco": "Rua Prudente de morais",
            "cep": "59150000",
            "cidade": "Natal",
            "bairro": "Tirol",
            "uf": "RN",
            "telefone": "",
        }
    }
)

response = wrapper.registra_boleto(data)

dump_response(response, os.path.basename(__file__).split(".")[0])
