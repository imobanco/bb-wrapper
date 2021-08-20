from unittest import TestCase

from bb_wrapper.services import PixCodeService
from bb_wrapper.services import QRCodeService


class PIXCodeServiceTestCase(TestCase):
    maxDiff = None

    def test_create(self):
        """
        https://forum.developers.bb.com.br/t/duvida-sobre-a-criacao-do-qrcode-da-cobranca-pix/4503/3?u=rodrigo3  # noqa

        Dado:
            - um location = "qrcodepix-h.bb.com.br/pix/v2/0c3f04a0-a41a-401e-8bb6-f6744c75a605"
            - um recebedor = "ALAN GUIACHERO BUENO"
        Quando:
            - for chamado PixCodeService().create(location, recebedor)
        Então:
            - deve ser retornado result_data e result_qrcode
            - result_data deve ser "00020101021226870014br.gov.bcb.pix2565qrcodepix-h.bb.com.br/pix/v2/0c3f04a0-a41a-401e-8bb6-f6744c75a6055204000053039865802BR5912ALANGUIACHER6005NATAL62070503***6304D592"  # noqa
            - result_qrcode deve ser QRCodeService().generate_qrcode_b64image(expected_data)
        """
        location = "qrcodepix-h.bb.com.br/pix/v2/0c3f04a0-a41a-401e-8bb6-f6744c75a605"
        recebedor = "ALAN GUIACHERO BUENO"

        result_data, result_qrcode = PixCodeService().create(location, recebedor)

        expected_data = """00020101021226870014br.gov.bcb.pix2565qrcodepix-h.bb.com.br/pix/v2/0c3f04a0-a41a-401e-8bb6-f6744c75a6055204000053039865802BR5912ALANGUIACHER6005NATAL62070503***6304D592"""  # noqa
        expected_qrcode = QRCodeService().generate_qrcode_b64image(expected_data)

        self.assertEqual(result_data, expected_data)
        self.assertEqual(result_qrcode, expected_qrcode)

    def test_create_2(self):
        """
        https://forum.developers.bb.com.br/t/duvida-sobre-a-criacao-do-qrcode-da-cobranca-pix/4503/3?u=rodrigo3  # noqa

        Dado:
            - um location = "qrcodepix.bb.com.br/pix/v2/e1503bee-684b-4952-ade3-78c0a47e1d0e"
            - um recebedor = "IMOBANCO"
        Quando:
            - for chamado PixCodeService().create(location, recebedor)
        Então:
            - deve ser retornado result_data e result_qrcode
            - result_data deve ser "00020101021226850014br.gov.bcb.pix2563qrcodepix.bb.com.br/pix/v2/e1503bee-684b-4952-ade3-78c0a47e1d0e5204000053039865802BR5908IMOBANCO6005NATAL62070503***63040965"  # noqa
            - result_qrcode deve ser QRCodeService().generate_qrcode_b64image(expected_data)
        """
        location = "qrcodepix.bb.com.br/pix/v2/e1503bee-684b-4952-ade3-78c0a47e1d0e"
        recebedor = "IMOBANCO"

        result_data, result_qrcode = PixCodeService().create(location, recebedor)

        expected_data = """00020101021226850014br.gov.bcb.pix2563qrcodepix.bb.com.br/pix/v2/e1503bee-684b-4952-ade3-78c0a47e1d0e5204000053039865802BR5908IMOBANCO6005NATAL62070503***63040965"""  # noqa
        expected_qrcode = QRCodeService().generate_qrcode_b64image(expected_data)

        self.assertEqual(result_data, expected_data)
        self.assertEqual(result_qrcode, expected_qrcode)
