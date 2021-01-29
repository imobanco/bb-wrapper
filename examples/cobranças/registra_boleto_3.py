import os
from datetime import date

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

number = "9999999995"

today = date.today()
bb_fmt = "%d.%m.%Y"

data = wrapper.create_boleto_data_with_defaults(
    {
        "dataEmissao": today.strftime(bb_fmt),
        "dataVencimento": today.strftime(bb_fmt),
        "valorOriginal": 3.0,
        "numeroTituloBeneficiario": number,
        "numeroTituloCliente": wrapper.build_our_number(number),
        "pagador": {
            "tipoInscricao": 1,
            "numeroInscricao": "71128590182",
            "nome": "NOME",
            "endereco": "ENDERECO",
            "cep": "70675727",
            "cidade": "SAO PAULO",
            "bairro": "CENTRO",
            "uf": "SP",
            "telefone": "999939669",
        },
        "avalista": {
            "tipoInscricao": 1,
            "numeroInscricao": "71128590182",
            "nome": "NOME",
        },
        "jurosMora": {"tipo": 1, "valor": 0.1},
    }
)

response = wrapper.registra_boleto(data)

dump_response(response, os.path.basename(__file__).split(".")[0])
