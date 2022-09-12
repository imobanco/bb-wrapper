from unittest.mock import MagicMock

from bb_wrapper.wrapper import PIXCobBBWrapper
from bb_wrapper.services import PixCodeService
from tests.utils import IsolatedEnvTestCase, MockedRequestsTestCase


class PixCobBBWrapperTestCase(IsolatedEnvTestCase, MockedRequestsTestCase):
    maxDiff = None

    def test_create_and_validate_cobranca_data_cpf(self):
        """
        Dado:
            - alguns inputs:
                expiracao = 61
                chave = "chave"
                documento = "12345678901"
                devedor = "devedor"
                valor = 15.5
                descricao = "descrição"
        Quando:
            - for chamado PIXCobBBWrapper()._create_and_validate_cobranca_data(
                    expiracao, chave, documento, devedor, valor, descricao
                )
        Então:
            - o resultado deve ser o dict
                {
                    "calendario": {"expiracao": expiracao},
                    "valor": {"original": valor},
                    "devedor": {"cpf": documento, "nome": devedor},
                    "chave": chave,
                    "solicitacaoPagador": descricao,
                }
        """
        expiracao = 61
        chave = "chave"
        documento = "12345678901"
        devedor = "devedor"
        valor = 15.5
        descricao = "descrição"

        result = PIXCobBBWrapper()._create_and_validate_cobranca_data(
            expiracao, chave, documento, devedor, valor, descricao
        )

        expected = {
            "calendario": {"expiracao": expiracao},
            "valor": {"original": valor},
            "devedor": {"cpf": documento, "nome": devedor},
            "chave": chave,
            "solicitacaoPagador": descricao,
        }

        self.assertEqual(result, expected)

    def test_create_and_validate_cobranca_data_cnpj(self):
        """
        Dado:
            - alguns inputs:
                expiracao = 61
                chave = "chave"
                documento = "12345678901234"
                devedor = "devedor"
                valor = 15.5
                descricao = "descrição"
        Quando:
            - for chamado PIXCobBBWrapper()._create_and_validate_cobranca_data(
                    expiracao, chave, documento, devedor, valor, descricao
                )
        Então:
            - o resultado deve ser o dict
                {
                    "calendario": {"expiracao": expiracao},
                    "valor": {"original": valor},
                    "devedor": {"cnpj": documento, "nome": devedor},
                    "chave": chave,
                    "solicitacaoPagador": descricao,
                }
        """
        expiracao = 61
        chave = "chave"
        documento = "12345678901234"
        devedor = "devedor"
        valor = 15.5
        descricao = "descrição"

        result = PIXCobBBWrapper()._create_and_validate_cobranca_data(
            expiracao, chave, documento, devedor, valor, descricao
        )

        expected = {
            "calendario": {"expiracao": expiracao},
            "valor": {"original": valor},
            "devedor": {"cnpj": documento, "nome": devedor},
            "chave": chave,
            "solicitacaoPagador": descricao,
        }

        self.assertEqual(result, expected)

    def test_create_and_validate_cobranca_data_wrong_document(self):
        """
        Dado:
            - alguns inputs:
                expiracao = 61
                chave = "chave"
                documento = "123"
                devedor = "devedor"
                valor = 15.5
                descricao = "descrição"
        Quando:
            - for chamado PIXCobBBWrapper()._create_and_validate_cobranca_data(
                    expiracao, chave, documento, devedor, valor, descricao
                )
        Então:
            - deve ser lançado um ValueError com
                "Tipo de documento não identificado!"
        """
        expiracao = 61
        chave = "chave"
        documento = "123"
        devedor = "devedor"
        valor = 15.5
        descricao = "descrição"

        with self.assertRaises(ValueError) as ctx:
            PIXCobBBWrapper()._create_and_validate_cobranca_data(
                expiracao, chave, documento, devedor, valor, descricao
            )

        self.assertEqual(ctx.exception.args[0], "Tipo de documento não identificado!")

    def test_injeta_qrcode_data(self):
        """
        Dado:
            - uma 'response' com
                data={"location": "location_qualquer"}
            - um 'nome' "Nome Qualquer"
        Quando:
            - for chamado PIXCobBBWrapper()._injeta_qrcode_data(response, nome)  # noqa: E501
        Então:
            - response.data["qrcode_data"] deve ser PixCodeService().create(response.data["location"], nome)[0]  # noqa: E501
            - response.data["qrcode_b64"] deve ser PixCodeService().create(response.data["location"], nome)[1]  # noqa: E501
        """

        response = MagicMock(data={"location": "location_qualquer"})

        nome = "Nome Qualquer"

        PIXCobBBWrapper()._injeta_qrcode_data(response, nome)

        expected_data, expected_b64 = PixCodeService().create(
            response.data["location"], nome
        )

        self.assertEqual(response.data["qrcode_data"], expected_data)
        self.assertEqual(response.data["qrcode_b64"], expected_b64)

    def test_construct_url_1(self):
        """
        Dado:
            -
        Quando:
            - for chamado PIXCobBBWrapper()._construct_url(end_bar=True, search=None)
        Então:
            - o resultado deve ter pelo menos o texto
                'https://api.hm.bb.com.br/pix/v1/?gw-dev-app-key='
        """
        result = PIXCobBBWrapper()._construct_url(end_bar=True)

        expected = "https://api.sandbox.bb.com.br/pix/v1/?gw-dev-app-key="

        self.assertIn(expected, result)

    def test_construct_url_2(self):
        """
        Dado:
            -
        Quando:
            - for chamado PIXCobBBWrapper()._construct_url(end_bar=False)
        Então:
            - o resultado deve ter pelo menos o texto
                'https://api.hm.bb.com.br/pix/v1?gw-dev-app-key='
        """
        result = PIXCobBBWrapper()._construct_url(end_bar=False)

        expected = "https://api.sandbox.bb.com.br/pix/v1?gw-dev-app-key="

        self.assertIn(expected, result)

    def test_consultar_cobranca_content_bizarro(self):
        """
        A string 'Mensalidade setembro (-5\n%)' em um content
        bytes para fazer o parse para JSON estoura um JSONDecodeError!
        """
        tx_id = "foo"

        content = b'{\n\t\n\t"status": "CONCLUIDA",\n\t"calendario": {\n\t\t"criacao": "2022-09-12T07:58:41.29-03:00",\n\t\t"expiracao": "604800"\n\t},\n\t"location": "qrcodepix.bb.com.br/pix/v2/46asd23a5-g5h6-j7k8-l9a0-adasd231r5bd",\n\t"txid": "eVShZasd1asd2rLTasdASDg44",\n\t"revisao": 0,\n\t\n\t\t"devedor": {\n\t\t\t\n\t\t\t\t"cpf": "00000000000",\n\t\t\t\n\t\t\t\n\t\t\t"nome": "DANIEL FULANO"\n\t\t},\n\t\n\t"valor": {\n\t\t"original": "902.50"\n\t},\n\t"chave": "asd27bd-4ag6-5fsc-y6hm-d1da25fa4bdsdf",\n\t\n\t\t"infoAdicionais": [\n\t\t\t\n\t\t\t{\n\t\t\t\t"nome": "Benefici\xc3\xa1rio final",\n\t\t\t\t"valor": "MARIA FULANO, cnpj: 00000000000000"\n\t\t\t}\n\t\t\t\n\t\t\t\n\t\t],\n\t\n\t\n\t\t"pix": [\n\t\t\t{\n\t\t\t\t"endToEndId": "E00000000202209121142123454564",\n\t\t\t\t"txid": "eKpVSLh0asdGasdM2DvrLTsqA4s4",\n\t\t\t\t"valor": "902.50",\n\t\t\t\t\n\t\t\t\t\t"pagador": {\n\t\t\t\t\t\t\n\t\t\t\t\t\t\t"cpf": "00000000000",\n\t\t\t\t\t\t\n\t\t\t\t\t\t\n\t\t\t\t\t\t"nome": "DANIEL FULANO"\n\t\t\t\t\t},\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\t"infoPagador": "Mensalidade setembro (-5\n%)",\n\t\t\t\t\n\t\t\t\t\n                "horario": "2022-09-12T08:43:39.00-03:00"\n\t\t\t}\n\t\t],\n\t\n\t"solicitacaoPagador": "MENSALIDADE SETEMBRO/22 - MATEUS FULANO"\n\t\n}'  # noqa

        url = PIXCobBBWrapper()._construct_url("cob", tx_id)
        self.mock_responses.add("GET", url, content, status=200)

        result = PIXCobBBWrapper().consultar_cobranca(tx_id)

        expected_data = {}

        self.assertNotEqual(result.data, expected_data)
        self.assertEqual(
            result.data["pix"][0]["infoPagador"], "Mensalidade setembro (-5\n%)"
        )
