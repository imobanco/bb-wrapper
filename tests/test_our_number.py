from unittest import TestCase

from bb_wrapper.number_utils import build_our_number


class OurNumberTestCase(TestCase):
    def test_1(self):
        """
        Dado:
            - convênio '1234567'
            - um número '0123456789'
        Quando:
            - for chamado build_our_number(number, convenio)
        Então:
            - o resultado deve ser f'000{convenio}{number}'
        """
        convenio = '1234567'

        number = '0123456789'

        result = build_our_number(number, convenio)

        expected = f'000{convenio}{number}'

        self.assertEqual(result, expected)

    def test_2(self):
        """
        Dado:
            - convênio '123456'
            - um número '0123456789'
        Quando:
            - for chamado build_our_number(number, convenio)
        Então:
            - o resultado deve ser f'000{convenio}{number}'
        """
        convenio = '123456'

        number = '0123456789'

        with self.assertRaises(AssertionError):
            build_our_number(number, convenio)

    def test_3(self):
        """
        Dado:
            - convênio '1234567'
            - um número '012345678'
        Quando:
            - for chamado build_our_number(number, convenio)
        Então:
            - o resultado deve ser f'000{convenio}{number}'
        """
        convenio = '1234567'

        number = '012345678'

        with self.assertRaises(AssertionError):
            build_our_number(number, convenio)
