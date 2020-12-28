import os

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

data = wrapper.create_boleto_data_with_defaults(
    {
        "dataEmissao": "07.12.2020",
        "dataVencimento": "07.12.2020",
        "valorOriginal": 100.00,
        "numeroTituloBeneficiario": "TESTE2",
        "numeroTituloCliente": "00031285571231230017",
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
        "desconto": {"tipo": 1, "dataExpiracao": "05.12.2020", "valor": 0.3},
        "segundoDesconto": {"dataExpiracao": "06.12.2020", "valor": 0.2},
        "terceiroDesconto": {"dataExpiracao": "07.12.2020", "valor": 0.1},
    }
)

response = wrapper.registra_boleto(data)

dump_response(response, os.path.basename(__file__).split(".")[0])
