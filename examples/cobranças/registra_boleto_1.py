import os
from datetime import date

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

number = 9999999983
today = date.today()
bb_fmt = "%d.%m.%Y"

data = wrapper.create_boleto_data_with_defaults(
    {
        "dataEmissao": today.strftime(bb_fmt),
        "dataVencimento": today.strftime(bb_fmt),
        "numeroDiasLimiteRecebimento": 15,
        "valorOriginal": 3.1,
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
        },
    }
)

response = wrapper.registra_boleto(data)

dump_response(response, os.path.basename(__file__).split(".")[0])
