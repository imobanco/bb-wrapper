from unittest import TestCase

from bb_wrapper.services import ModService


class ModServiceTestCase(TestCase):
    def test_modulo10_1(self):
        """
        Dado:
            - um número "1"
        Quando:
            - for chamado ModService().modulo10(number)
        Então:
            - o resultado deve ser 8
        """
        number = "1"

        result = ModService().modulo10(number)

        expected = 8

        self.assertEqual(result, expected)

    def test_modulo10_2(self):
        """
        Dado:
            - um número "2"
        Quando:
            - for chamado ModService().modulo10(number)
        Então:
            - o resultado deve ser 6
        """
        number = "2"

        result = ModService().modulo10(number)

        expected = 6

        self.assertEqual(result, expected)

    def test_modulo10_3(self):
        """
        Dado:
            - um número "12"
        Quando:
            - for chamado ModService().modulo10(number)
        Então:
            - o resultado deve ser 5
        """
        number = "12"

        result = ModService().modulo10(number)

        expected = 5

        self.assertEqual(result, expected)

    def test_modulo10_4(self):
        """
        Dado:
            - um número "21"
        Quando:
            - for chamado ModService().modulo10(number)
        Então:
            - o resultado deve ser 6
        """
        number = "21"

        result = ModService().modulo10(number)

        expected = 6

        self.assertEqual(result, expected)

    def test_modulo11_1(self):
        """
        Dado:
            - um número "1"
        Quando:
            - for chamado ModService().modulo11(number)
        Então:
            - o resultado deve ser 2
        """
        number = "1"

        result = ModService().modulo11(number)

        expected = 2

        self.assertEqual(result, expected)

    def test_modulo11_2(self):
        """
        Dado:
            - um número "2"
        Quando:
            - for chamado ModService().modulo11(number)
        Então:
            - o resultado deve ser 7
        """
        number = "2"

        result = ModService().modulo11(number)

        expected = 4

        self.assertEqual(result, expected)

    def test_modulo11_3(self):
        """
        Dado:
            - um número "12"
        Quando:
            - for chamado ModService().modulo11(number)
        Então:
            - o resultado deve ser 7
        """
        number = "12"

        result = ModService().modulo11(number)

        expected = 7

        self.assertEqual(result, expected)

    def test_modulo11_4(self):
        """
        Dado:
            - um número "21"
        Quando:
            - for chamado ModService().modulo11(number)
        Então:
            - o resultado deve ser 8
        """
        number = "21"

        result = ModService().modulo11(number)

        expected = 8

        self.assertEqual(result, expected)

    def test_modulo11_5(self):
        """
        Dado:
            - um número "1"
        Quando:
            - for chamado ModService().modulo11(number, r_base=1)
        Então:
            - o resultado deve ser 9
        """
        number = "1"

        result = ModService().modulo11(number, multiply_by_10_flag=False)

        expected = 9

        self.assertEqual(result, expected)

    def test_modulo11_6(self):
        """
        Dado:
            - um número "2"
        Quando:
            - for chamado ModService().modulo11(number, r_base=1)
        Então:
            - o resultado deve ser 7
        """
        number = "2"

        result = ModService().modulo11(number, multiply_by_10_flag=False)

        expected = 7

        self.assertEqual(result, expected)

    def test_modulo11_7(self):
        """
        Dado:
            - um número "12"
        Quando:
            - for chamado ModService().modulo11(number, r_base=1)
        Então:
            - o resultado deve ser 4
        """
        number = "12"

        result = ModService().modulo11(number, multiply_by_10_flag=False)

        expected = 4

        self.assertEqual(result, expected)

    def test_modulo11_8(self):
        """
        Dado:
            - um número "21"
        Quando:
            - for chamado ModService().modulo11(number, r_base=1)
        Então:
            - o resultado deve ser 3
        """
        number = "21"

        result = ModService().modulo11(number, multiply_by_10_flag=False)

        expected = 3

        self.assertEqual(result, expected)
