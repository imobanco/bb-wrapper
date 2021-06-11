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

    def test_crc_16_ccitt_ffff_1(self):
        """
        https://forum.developers.bb.com.br/t/duvida-sobre-a-criacao-do-qrcode-da-cobranca-pix/4503/3?u=rodrigo3

        Dado:
            - um data ALTAMENTE MÁGICO
        Quando:
            - for chamado BRCodeService().crc_16_ccitt_ffff(data)
        Então:
            - o resultado deve ser
        """
        data = """00020101021226870014br.gov.bcb.pix2565qrcodepix-h.bb.com.br/pix/v2/0c3f04a0-a41a-401e-8bb6-f6744c75a6055204000053039865802BR5920ALAN GUIACHERO BUENO6008BRASILIA62070503***6304"""  # noqa

        result = BRCodeService().crc_16_ccitt_ffff(data)

        expected = "2AC9"

        self.assertEqual(result, expected)

    def test_crc_16_ccitt_ffff_2(self):
        """
        https://forum.developers.bb.com.br/t/duvida-sobre-a-criacao-do-qrcode-da-cobranca-pix/4503/3?u=rodrigo3

        Dado:
            - um data ALTAMENTE MÁGICO
        Quando:
            - for chamado BRCodeService().crc_16_ccitt_ffff(data)
        Então:
            - o resultado deve ser
        """
        data = """00020101021226700014br.gov.bcb.pix2548pix.example.com/8b3da2f39a4140d1a91abd93113bd4415204000053039865802BR5913Fulano de Tal6008BRASILIA62070503***6304"""  # noqa

        result = BRCodeService().crc_16_ccitt_ffff(data)

        expected = "64E4"

        self.assertEqual(result, expected)
