import os
from datetime import date, timedelta

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

number = "9999999992"

today = date.today()
bb_fmt = "%d.%m.%Y"

data = wrapper.create_boleto_data_with_defaults(
    {
        "dataEmissao": today.strftime(bb_fmt),
        "dataVencimento": today.strftime(bb_fmt),
        "valorOriginal": 50.0,
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
        "multa": {
            "tipo": 2,
            "porcentagem": 0.1,
            "data": (today + timedelta(days=1)).strftime(bb_fmt),
        },
        "desconto": {
            "tipo": 1,
            "dataExpiracao": (today - timedelta(days=2)).strftime(bb_fmt),
            "valor": 1.3,
        },
        "segundoDesconto": {
            "dataExpiracao": (today - timedelta(days=1)).strftime(bb_fmt),
            "valor": 1.2,
        },
        "terceiroDesconto": {"dataExpiracao": today.strftime(bb_fmt), "valor": 1.1},
    }
)

response = wrapper.registra_boleto(data)

dump_response(response, os.path.realpath(__file__))
