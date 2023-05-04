from py_bdd_context import BDDContextTestCase
from bb_wrapper.services.pix import PixService
from bb_wrapper.models.pagamentos import TipoChavePIX


class PixServiceTestCase(BDDContextTestCase):
    def test_is_email(self):
        with self.given(
            """
                - uma chave 'test@test.com'
            """
        ):
            email = "test@test.com"

        with self.when(
            """
                - for utilizado o service de PIX para identificação do tipo da chave
            """
        ):
            result = PixService().identify_key_type(email)

        with self.then(
            """
                - o tipo da chave identificado deve ser email
            """
        ):
            expected = TipoChavePIX.email
            self.assertEqual(result, expected)

    def test_is_phone(self):
        with self.given(
            """
                - uma chave '11999887766'
            """
        ):
            phone = "11999887766"
        with self.when(
            """
                - for utilizado o service de PIX para identificação do tipo da chave
            """
        ):
            result = PixService().identify_key_type(phone)
        with self.then(
            """
                - o tipo da chave identificado deve ser telefone
            """
        ):
            expected = TipoChavePIX.telefone
            self.assertEqual(result, expected)

    def test_is_uuid(self):
        with self.given(
            """
                - uma chave '45abb60a-6253-4f22-802b-0d84045ea76a'
            """
        ):
            uuid = "45abb60a-6253-4f22-802b-0d84045ea76a"
        with self.when(
            """
                - for utilizado o service de PIX para identificação do tipo da chave
            """
        ):
            result = PixService().identify_key_type(uuid)
        with self.then(
            """
                - o tipo da chave identificado deve ser uuid
            """
        ):
            expected = TipoChavePIX.uuid
            self.assertEqual(result, expected)

    def test_is_cnpj(self):
        with self.given(
            """
                - uma chave '03794722000153'
            """
        ):
            cnpj = "03794722000153"
        with self.when(
            """
                - for utilizado o service de PIX para identificação do tipo da chave
            """
        ):
            result = PixService().identify_key_type(cnpj)
        with self.then(
            """
                - o tipo da chave identificado deve ser documento
            """
        ):
            expected = TipoChavePIX.documento
            self.assertEqual(result, expected)

    def test_is_cpf(self):
        with self.given(
            """
                - uma chave '43166663045'
            """
        ):
            cpf = "43166663045"
        with self.when(
            """
                - for utilizado o service de PIX para identificação do tipo da chave
            """
        ):
            result = PixService().identify_key_type(cpf)
        with self.then(
            """
                - o tipo da chave identificado deve ser documento
            """
        ):
            expected = TipoChavePIX.documento
            self.assertEqual(result, expected)

    def test_is_not_key(self):
        with self.given(
            """
                - uma chave '1'
            """
        ):
            key_invalid = "1"

        with self.when(
            """
                - for utilizado o service de PIX para identificação do tipo da chave
            """
        ):
            with self.assertRaises(ValueError) as ctx:
                PixService().identify_key_type(key_invalid)
        with self.then(
            """
                - deve ser levantada uma exceção informando que a chave informada é inválida # noqa
            """
        ):
            self.assertEqual(ctx.exception.args[0], "Tipo de chave não identificado")

    def test_email_valid(self):
        with self.given(
            """
                - um email 'test@test.com'
            """
        ):
            email = "test@test.com"

        with self.when(
            """
                - o service de PIX para verificar email for chamado
            """
        ):
            result = PixService().verify_email(email)

        with self.then(
            """
                - o service deve retornar que o email informado é válido
            """
        ):
            self.assertTrue(result)

    def test_email_invalid(self):
        with self.given(
            """
                - um email 'teste@...br'
            """
        ):
            email = "teste@...br"

        with self.when(
            """
                - o service de PIX para verificar email for chamado
            """
        ):
            with self.assertRaises(ValueError) as ctx:
                PixService().verify_email(email)

        with self.then(
            """
                - deve ser levantada uma exceção informando que o email é inválido
            """
        ):
            self.assertEqual(ctx.exception.args[0], "Email inválido!")
