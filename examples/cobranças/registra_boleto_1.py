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
            "nome": "Nome' do João da Mária",
            "endereco": "Rua Joazeirão da Sílva 1º",
            "cep": "70675727",
            "cidade": "São Paulo",
            "bairro": "Centro",
            "uf": "SP",
            "telefone": "999939669",
        },
        "email": "cliente@email.com",
    }
)

response = wrapper.registra_boleto(data)

dump_response(response, os.path.basename(__file__).split(".")[0])
