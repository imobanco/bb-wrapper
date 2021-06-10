from unittest import TestCase

from bb_wrapper.services.brcode import BRCodeService


class BRCodeServiceTestCase(TestCase):
    maxDiff = None

    def test_len_zfilled_1(self):
        """
        Dado:
            - um 'data' '123'
        Quando:
            - for chamado BRCodeService()._get_len_zfilled(data)
        Então:
            - o resultado deve ser "03"
        """
        data = "123"

        result = BRCodeService()._get_len_zfilled(data)

        expected = "03"

        self.assertEqual(result, expected)

    def test_len_zfilled_2(self):
        """
        Dado:
            - um 'data' '1234567890123456789'
        Quando:
            - for chamado BRCodeService()._get_len_zfilled(data)
        Então:
            - o resultado deve ser "19"
        """
        data = "1234567890123456789"

        result = BRCodeService()._get_len_zfilled(data)

        expected = "19"

        self.assertEqual(result, expected)

    def test_create_field_string_1(self):
        """
        Dado:
            - um '_id' "ID"
            - um 'value' "|127.0.0.0"
        Quando:
            - for chamado BRCodeService().create_field_string(_id, value)
        Então:
            - o resultado deve ser "ID10|127.0.0.0"
        """
        _id = "ID"
        value = "|127.0.0.0"

        result = BRCodeService().create_field_string(_id, value)

        expected = "ID10|127.0.0.0"

        self.assertEqual(result, expected)
