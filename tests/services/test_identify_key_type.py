from py_bdd_context import BDDContextTestCase
from bb_wrapper.services.pix import PixService


class PixServiceTestCase(BDDContextTestCase):
    def test_is_email(self):
        with self.given(
            """
            - Uma string 'test@test.com'
            """
        ):
            email = "test@test.com"
        with self.when(
            """
            - PixService().identify_key_type('test@test.com')
            """
        ):
            result = PixService().identify_key_type(email)
        with self.then(
            """
            - O resultado deve ser 2
            """
        ):
            expected = 2
            self.assertEqual(result, expected)

    def test_is_phone(self):
        with self.given(
            """
            - Uma string 'phone'
            """
        ):
            phone = "11999887766"
        with self.when(
            """
            - PixService().identify_key_type(phone)
            """
        ):
            result = PixService().identify_key_type(phone)
        with self.then(
            """
            - O resultado deve ser 1
            """
        ):
            expected = 1
            self.assertEqual(result, expected)

    def test_is_uuid(self):
        with self.given(
            """
            - Uma string 'uuid'
            """
        ):
            uuid = "45abb60a-6253-4f22-802b-0d84045ea76a"
        with self.when(
            """
            - PixService().identify_key_type(uuid)
            """
        ):
            result = PixService().identify_key_type(uuid)
        with self.then(
            """
            - O resultado deve ser 4
            """
        ):
            expected = 4
            self.assertEqual(result, expected)

    def test_is_cnpj(self):
        with self.given(
            """
            - Uma string '03794722000153'
            """
        ):
            cnpj = "03794722000153"
        with self.when(
            """
            - PixService().identify_key_type("03794722000153")
            """
        ):
            result = PixService().identify_key_type(cnpj)
        with self.then(
            """
            - O resultado deve ser 4
            """
        ):
            expected = 3
            self.assertEqual(result, expected)

    def test_is_cpf(self):
        with self.given(
            """
            - Uma string '43166663045'
            """
        ):
            cpf = "43166663045"
        with self.when(
            """
            - PixService().identify_key_type("43166663045")
            """
        ):
            result = PixService().identify_key_type(cpf)
        with self.then(
            """
            - O resultado deve ser 4
            """
        ):
            expected = 3
            self.assertEqual(result, expected)

    def test_is_not_key(self):
        with self.given(
            """
            -  Dado uma string '1'
            """
        ):
            key_invalid = "1"
        with self.when(
            """
            - PixService().identify_key_type("1")
            """
        ):
            with self.assertRaises(ValueError) as ctx:
                PixService().identify_key_type(key_invalid)
        with self.then(
            """
            - Deve ser lançado um ValueError com "Tipo de chave não identificado"
            """
        ):
            self.assertEqual(ctx.exception.args[0], "Tipo de chave não identificado")

    def test_email_valid(self):
        with self.given(
            """
            - Uma string 'test@test.com'
            """
        ):
            email = "test@test.com"
        with self.when(
            """
            - PixService().verify_email('test@test.com')
            """
        ):
            result = PixService().verify_email(email)
        with self.then(
            """
            - O resultado deve ser True
            """
        ):
            self.assertTrue(result)

    def test_email_invalid(self):
        with self.given(
            """
            - Uma string 'teste@...br'
            """
        ):
            email = "teste@...br"
        with self.when(
            """
            - PixService().verify_email('teste@...br')
            """
        ):
            with self.assertRaises(ValueError) as ctx:
                PixService().verify_email(email)
        with self.then(
            """
            - O resultado deve ser True
            """
        ):
            self.assertEqual(ctx.exception.args[0], "Email inválido!")
