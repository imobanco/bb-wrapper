from unittest import TestCase

from bb_wrapper.utils import parse_unicode_to_alphanumeric


class ParseUnicodeToAsciiTestCase(TestCase):
    def test_1(self):
        """
        Dado:
            - um texto "ÁÑàÙçþíÍ1µŋß?°ŧŋ"
        Quando:
            - for chamado parse_unicode_to_ascii(text)
        Então:
            - o resultado deve ser "ANAUCTHII1UNGSSDEGTNG"
        """
        text = "Á'`ÑàÙçþíÍ1µŋß?°ŧŋ_"

        result = parse_unicode_to_alphanumeric(text)

        expected = "ANAUCTHII1UNGSSDEGTNG"

        self.assertEqual(result, expected)
