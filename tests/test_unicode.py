from unittest import TestCase

from bb_wrapper.utils import parse_unicode_to_ascii


class ParseUnicodeToAsciiTestCase(TestCase):
    def test_1(self):
        """
        Dado:
            - um texto "ÁÑàÙçþíÍ1µŋß?°ŧŋ"
        Quando:
            - for chamado parse_unicode_to_ascii(text)
        Então:
            - o resultado deve ser ¯\_(ツ)_/¯  # noqa
        """
        text = "Á'`ÑàÙçþíÍ1µŋß?°ŧŋ"

        result = parse_unicode_to_ascii(text)

        expected = "A'`NAUCTHII1UNGSS?DEGTNG"

        self.assertEqual(result, expected)
