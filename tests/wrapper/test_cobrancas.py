from unittest import TestCase

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper


class OurNumberTestCase(TestCase):
    def test_convenio_assert(self):
        with self.assertRaises(AssertionError) as ctx:
            CobrancasBBWrapper(convenio="123")

        self.assertEqual(ctx.exception.args[0], "O convênio não possui 7 dígitos!")

    def test_build_our_number_1(self):
        """
        Dado:
            - convênio '1234567'
            - um número '0123456789'
            - um wrapper CobrancasBBWrapper com
                convenio=convenio
        Quando:
            - for chamado build_our_number(our_number)
        Então:
            - o resultado deve ser f'000{convenio}{our_number}'
        """
        convenio = "1234567"

        number = "0123456789"

        wrapper = CobrancasBBWrapper(convenio=convenio)

        result = wrapper.build_our_number(number)

        expected = f"000{convenio}{number}"

        self.assertEqual(result, expected)

    def test_build_our_number_2(self):
        """
        Dado:
            - convênio '1234567'
            - um número '012345678'
            - um wrapper CobrancasBBWrapper com
                convenio=convenio
        Quando:
            - for chamado build_our_number(our_number)
        Então:
            - o resultado deve ser f'000{convenio}{our_number}'
        """
        convenio = "1234567"

        number = "012345678"

        wrapper = CobrancasBBWrapper(convenio=convenio)

        with self.assertRaises(AssertionError) as ctx:
            wrapper.build_our_number(number)

        self.assertEqual(ctx.exception.args[0], "O número não tem 10 dígitos!")

    def test_create_boleto_data_with_defaults_1(self):
        """
        Dado:
            -
        Quando:
            -
        Então:
            -
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
            "indicadorNumeroDiasLimiteRecebimento": "N",
            "numeroDiasLimiteRecebimento": 0,
            "codigoAceite": "N",
            "codigoTipoTitulo": 4,
            "indicadorPermissaoRecebimentoParcial": "N",
        }

        result = wrapper.create_boleto_data_with_defaults(data)

        self.assertEqual(result, expected)

    def test_create_boleto_data_with_defaults_2(self):
        """
        Dado:
            -
        Quando:
            -
        Então:
            -
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
            "indicadorNumeroDiasLimiteRecebimento": "N",
            "numeroDiasLimiteRecebimento": 0,
            "codigoAceite": "N",
            "codigoTipoTitulo": 4,
            "indicadorPermissaoRecebimentoParcial": "N",
        }

        result = wrapper.create_boleto_data_with_defaults(data)

        self.assertEqual(result, expected)
