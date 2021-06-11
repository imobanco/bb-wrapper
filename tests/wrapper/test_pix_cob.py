from unittest import TestCase
from unittest.mock import MagicMock

from bb_wrapper.wrapper import PIXCobBBWrapper
from bb_wrapper.services import PixCodeService


class PixCobBBWrapperTestCase(TestCase):
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

    def test_injetar_qrcode_data_na_cobranca(self):
        """
        Dado:
            - uma 'response' com
                data={"location": "location_qualquer"}
            - um 'nome' "Nome Qualquer"
        Quando:
            - for chamado PIXCobBBWrapper()._injetar_qrcode_data_na_cobranca(response, nome)  # noqa: E501
        Então:
            - response.data["qrcode_data"] deve ser PixCodeService().create(response.data["location"], nome)[0]  # noqa: E501
            - response.data["qrcode_b64"] deve ser PixCodeService().create(response.data["location"], nome)[1]  # noqa: E501
        """

        response = MagicMock(data={"location": "location_qualquer"})

        nome = "Nome Qualquer"

        PIXCobBBWrapper()._injetar_qrcode_data_na_cobranca(response, nome)

        expected_data, expected_b64 = PixCodeService().create(
            response.data["location"], nome
        )

        self.assertEqual(response.data["qrcode_data"], expected_data)
        self.assertEqual(response.data["qrcode_b64"], expected_b64)
