from unittest import TestCase
from unittest.mock import MagicMock

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper
from bb_wrapper.constants import GW_APP_KEY
from bb_wrapper.services import QRCodeService, BarcodeService


class CobrancasBBWrapperTestCase(TestCase):
    maxDiff = None

    def test_convenio_assert(self):
        """
        Dado:
            - um número de convenio="123" (inválido pois não tem 7 dígitos)
        Quando:
            - for chamado CobrancasBBWrapper(convenio="123")
        Então:
            - deve ser lançado `AssertionError`
            - a mensagem de erro deve ser 'O convênio não possui 7 dígitos!'
        """
        with self.assertRaises(AssertionError) as ctx:
            CobrancasBBWrapper(convenio="123")

        self.assertEqual(ctx.exception.args[0], "O convênio não possui 7 dígitos!")

    def test_build_our_number_1(self):
        """
        Dado:
            - convênio '1234567'
            - um número '1'
            - um wrapper CobrancasBBWrapper com
                convenio=convenio
        Quando:
            - for chamado build_our_number(our_number)
        Então:
            - o resultado deve ser f'000{convenio}000000000{number}'
        """
        convenio = "1234567"

        number = "1"

        wrapper = CobrancasBBWrapper(convenio=convenio)

        result = wrapper.build_our_number(number)

        expected = f"000{convenio}000000000{number}"

        self.assertEqual(result, expected)

    def test_build_our_number_2(self):
        """
        Dado:
            - convênio '1234567'
            - um número '123456789'
            - um wrapper CobrancasBBWrapper com
                convenio=convenio
        Quando:
            - for chamado build_our_number(our_number)
        Então:
            - o resultado deve ser f'000{convenio}0{number}'
        """
        convenio = "1234567"

        number = "123456789"

        wrapper = CobrancasBBWrapper(convenio=convenio)

        result = wrapper.build_our_number(number)

        expected = f"000{convenio}0{number}"

        self.assertEqual(result, expected)

    def test_build_our_number_3(self):
        """
        Dado:
            - convênio '1234567'
            - um número '01234567890'
            - um wrapper CobrancasBBWrapper com
                convenio=convenio
        Quando:
            - for chamado build_our_number(our_number)
        Então:
            - deve ser lançado `AssertionError`
            - a mensagem de erro deve ser "O número não tem 10 dígitos!"
        """
        convenio = "1234567"

        number = "01234567890"

        wrapper = CobrancasBBWrapper(convenio=convenio)

        with self.assertRaises(AssertionError) as ctx:
            wrapper.build_our_number(number)

        self.assertEqual(ctx.exception.args[0], "O número não tem 10 dígitos!")

    def test_create_boleto_data_with_defaults_1(self):
        """
        Dado:
            - um convenio "1234567"
            - uma carteira "17"
            - uma variacao_carteira = "35"
            - um wrapper CobrancasBBWrapper com
                convenio=convenio
                carteira=carteira
                variacao_carteira=variacao_carteira
            - um dict de dados 'data'
                {}
        Quando:
            - for chamado wrapper.create_boleto_data_with_defaults(data)
        Então:
            - o dict de resultado deve ser os valores padrões ¯\_(ツ)_/¯  # noqa
        """
        convenio = "1234567"
        carteira = "17"
        variacao_carteira = "35"

        wrapper = CobrancasBBWrapper(
            convenio=convenio, carteira=carteira, variacao_carteira=variacao_carteira
        )

        data = {}

        expected = {
            "numeroConvenio": convenio,
            "numeroCarteira": carteira,
            "numeroVariacaoCarteira": variacao_carteira,
            "codigoModalidade": 1,
            "quantidadeDiasProtesto": 0,
            "indicadorAceiteTituloVencido": "S",
            "numeroDiasLimiteRecebimento": 0,
            "codigoAceite": "N",
            "codigoTipoTitulo": 4,
            "indicadorPermissaoRecebimentoParcial": "N",
            "descricaoTipoTitulo": "DM",
            "indicadorPix": "S",
        }

        result = wrapper.create_boleto_data_with_defaults(data)

        self.assertEqual(result, expected)

    def test_create_boleto_data_with_defaults_2(self):
        """
        Dado:
            - um convenio "1234567"
            - uma carteira "17"
            - uma variacao_carteira = "35"
            - um wrapper CobrancasBBWrapper com
                convenio=convenio
                carteira=carteira
                variacao_carteira=variacao_carteira
            - um dict de dados 'data'
                {
                    "numeroConvenio": "1",
                    "numeroCarteira": "2",
                    "numeroVariacaoCarteira": "3",
                }
        Quando:
            - for chamado wrapper.create_boleto_data_with_defaults(data)
        Então:
            - o dict de resultado deve ter os valores do data sobreescritos ¯\_(ツ)_/¯  # noqa
        """
        convenio = "1234567"
        carteira = "17"
        variacao_carteira = "35"

        wrapper = CobrancasBBWrapper(
            convenio=convenio, carteira=carteira, variacao_carteira=variacao_carteira
        )

        data = {
            "numeroConvenio": "1",
            "numeroCarteira": "2",
            "numeroVariacaoCarteira": "3",
        }

        expected = {
            "numeroConvenio": "1",
            "numeroCarteira": "2",
            "numeroVariacaoCarteira": "3",
            "codigoModalidade": 1,
            "quantidadeDiasProtesto": 0,
            "indicadorAceiteTituloVencido": "S",
            "numeroDiasLimiteRecebimento": 0,
            "codigoAceite": "N",
            "codigoTipoTitulo": 4,
            "indicadorPermissaoRecebimentoParcial": "N",
            "descricaoTipoTitulo": "DM",
            "indicadorPix": "S",
        }

        result = wrapper.create_boleto_data_with_defaults(data)

        self.assertEqual(result, expected)

    def test_create_boleto_data_with_defaults_3(self):
        """
        Dado:
            - um convenio "1234567"
            - uma carteira "17"
            - uma variacao_carteira = "35"
            - um wrapper CobrancasBBWrapper com
                convenio=convenio
                carteira=carteira
                variacao_carteira=variacao_carteira
            - um dict de dados 'data'
                {
                    "textoCampoUtilizacaoBeneficiario": "Á'`ÑàÙçþíÍ1µŋß?°ŧŋ",
                    "textoMensagemBloquetoOcorrencia":  "Á'`ÑàÙçþíÍ1µŋß?°ŧŋ",
                }
        Quando:
            - for chamado wrapper.create_boleto_data_with_defaults(data)
        Então:
            - o dict de resultado deve ter os textos não-ascii transliterados em ascii ¯\_(ツ)_/¯  # noqa
        """
        convenio = "1234567"
        carteira = "17"
        variacao_carteira = "35"

        wrapper = CobrancasBBWrapper(
            convenio=convenio, carteira=carteira, variacao_carteira=variacao_carteira
        )

        data = {
            "textoCampoUtilizacaoBeneficiario": "Á'`ÑàÙçþíÍ1µŋß?°ŧŋ",
            "textoMensagemBloquetoOcorrencia": "Á'`ÑàÙçþíÍ1µŋß?°ŧŋ",
        }

        expected = {
            "numeroConvenio": convenio,
            "numeroCarteira": carteira,
            "numeroVariacaoCarteira": variacao_carteira,
            "codigoModalidade": 1,
            "quantidadeDiasProtesto": 0,
            "indicadorAceiteTituloVencido": "S",
            "numeroDiasLimiteRecebimento": 0,
            "codigoAceite": "N",
            "codigoTipoTitulo": 4,
            "indicadorPermissaoRecebimentoParcial": "N",
            "descricaoTipoTitulo": "DM",
            "indicadorPix": "S",
            "textoCampoUtilizacaoBeneficiario": "ANAUCTHII1UNGSSDEGTNG",
            "textoMensagemBloquetoOcorrencia": "ANAUCTHII1UNGSSDEGTNG",
        }

        result = wrapper.create_boleto_data_with_defaults(data)

        self.assertEqual(result, expected)

    def test_build_url(self):
        """
        Dado:
            - um wrapper CobrancasBBWrapper()
        Quando:
            - for chamado wrapper._construct_url()
        Então:
            - o resultado deve ser
                "https://api.sandbox.bb.com.br/cobrancas/v2/boletos"
                f"?gw-dev-app-key={GW_APP_KEY}"
        """
        wrapper = CobrancasBBWrapper()
        result = wrapper._construct_url()

        expected = (
            "https://api.sandbox.bb.com.br/cobrancas/v2/boletos"
            f"?gw-dev-app-key={GW_APP_KEY}"
        )

        self.assertEqual(result, expected)

    def test_injeta_b64_images_with_qrcode(self):
        """
        Dado:
            - uma 'response' com
                data={"location": "location_qualquer"}
        Quando:
            - for chamado PIXCobBBWrapper()._injetar_qrcode_data_na_cobranca(response, nome)  # noqa: E501
        Então:
            - response.data["qrcode_data"] deve ser PixCodeService().create(response.data["location"], nome)[0]  # noqa: E501
            - response.data["qrcode_b64"] deve ser PixCodeService().create(response.data["location"], nome)[1]  # noqa: E501
        """

        response = MagicMock(
            data={"codigoBarraNumerico": "123455123", "qrCode": {"emv": "emv_qualquer"}}
        )

        CobrancasBBWrapper()._injeta_b64_images(response)

        expected_barcode_b64 = BarcodeService().generate_barcode_b64image(
            response.data["codigoBarraNumerico"]
        )
        expected_qrcode_b64 = QRCodeService().generate_qrcode_b64image(
            response.data["qrCode"]["emv"]
        )

        self.assertEqual(response.data["codigo_barras_b64"], expected_barcode_b64)
        self.assertEqual(response.data["qrCode"]["b64"], expected_qrcode_b64)
