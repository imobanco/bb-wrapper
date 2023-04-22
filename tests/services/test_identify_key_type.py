from unittest import TestCase

from bb_wrapper.services.pix import PixService


class PixServiceTestCase(TestCase):
    def test_is_email(self):
        """
        Dado:
            - Dado uma string 'test@test.com'
        Quando:
            - for chamado PixService().identify_key_type('test@test.com')
        Então:
            - o resultado deve ser 2
        """
        email = "test@test.com"

        result = PixService().identify_key_type(email)

        expected = 2

        self.assertEqual(result, expected)

    def test_is_phone(self):
        """
        Dado:
            - Dado uma string 'phone'
        Quando:
            - for chamado PixService().identify_key_type(phone)
        Então:
            - o resultado deve ser 1
        """
        phone = "11999887766"

        result = PixService().identify_key_type(phone)

        expected = 1

        self.assertEqual(result, expected)

    def test_is_uuid(self):
        """
        Dado:
            - Dado uma string 'uuid'
        Quando:
            - for chamado PixService().identify_key_type(uuid)
        Então:
            - o resultado deve ser 4
        """
        uuid = "45abb60a-6253-4f22-802b-0d84045ea76a"

        result = PixService().identify_key_type(uuid)

        expected = 4

        self.assertEqual(result, expected)

    def test_is_cnpj(self):
        """
        Dado:
            - Dado uma string 'cnpj'
        Quando:
            - for chamado PixService().identify_key_type(cnpj)
        Então:
            - o resultado deve ser 4
        """
        cnpj = "03794722000153"

        result = PixService().identify_key_type(cnpj)

        expected = 3

        self.assertEqual(result, expected)

    def test_is_cpf(self):
        """
        Dado:
            - Dado uma string 'cpf'
        Quando:
            - for chamado PixService().identify_key_type(cpf)
        Então:
            - o resultado deve ser 4
        """
        cpf = "43166663045"

        result = PixService().identify_key_type(cpf)

        expected = 3

        self.assertEqual(result, expected)

    def test_is_not_key(self):
        """
        Dado:
            - Dado uma string 'key_invalid'
        Quando:
            - for chamado PixService().identify_key_type(key_invalid)
        Então:
            - deve ser lançado um ValueError com
                "Tipo de chave não identificado"
        """
        key_invalid = "1"

        with self.assertRaises(ValueError) as ctx:
            PixService().identify_key_type(key_invalid)

        self.assertEqual(ctx.exception.args[0], "Tipo de chave não identificado")
