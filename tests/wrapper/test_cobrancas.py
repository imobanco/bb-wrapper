from unittest import TestCase

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper


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
            "indicadorNumeroDiasLimiteRecebimento": "N",
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
            "indicadorNumeroDiasLimiteRecebimento": "N",
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
            "indicadorNumeroDiasLimiteRecebimento": "N",
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
